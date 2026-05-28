import hashlib
import secrets
import os
import json
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Request, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import engine, Base, get_db
from models import User, Document, History
from schemas import UserCreate, UserOut, Token, DocumentOut, HistoryOut, RenameRequest, QAOut, QARequest
from services.document_parser import parse_document
from services.text_splitter import split_text
from services.vector_store import add_to_vector_store, delete_from_vector_store
from services.qa_service import answer_question

import shutil
import uuid
from pathlib import Path

load_dotenv()

# 配置文件
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时有效

# 密码加密函数
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    return salt + ":" + hashlib.sha256((salt + password).encode()).hexdigest()

# 密码验证函数
def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt, hash_value = hashed_password.split(":")
    return hash_value == hashlib.sha256((salt + plain_password).encode()).hexdigest()


# JWT 工具函数
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 创建 JWT 访问令牌
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 获取当前用户
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id: int = int(user_id_str)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


# FastAPI 应用初始化
Base.metadata.create_all(bind=engine)
os.makedirs("uploads", exist_ok=True)

app = FastAPI()

# 跨域资源共享（CORS）中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 注册接口
@app.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=409, detail="该邮箱已被注册")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=409, detail="该用户名已被使用")

    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# 读取当前登录用户信息接口
@app.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

# 上传文件接口,保存文件 → 解析 → 分块 → 入库
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    user_dir = Path("uploads") / str(current_user.id)#拼接路径
    user_dir.mkdir(parents=True, exist_ok=True)#.mkdir()用于创建目录,不存在就创建（包括父目录），已存在就跳过

    ext = Path(file.filename).suffix.lower()#获取Path对象的文件扩展名并转换为小写
    if ext not in {".pdf", ".docx", ".txt", ".md"}:
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    #两个用户可能上传同名文件(都叫报告.pdf),直接用原始文件名会互相覆盖.用 UUID 重命名彻底避免了冲突.
    unique_name = f"{uuid.uuid4().hex}{ext}"#uuid4()生成一个随机的 UUID(通用唯一标识符),.hex将UUID转换为十六进制字符串,f-string 把 .hex 和扩展名拼在一起
    # 保存文件到指定目录
    file_path = user_dir / unique_name

    with open(file_path, "wb") as buffer:#以写入模式打开buffer磁盘文件对象
        shutil.copyfileobj(file.file, buffer)#把上传的文件拷贝到buffer磁盘文件对象

    # 获取文件大小
    file_size = file_path.stat().st_size

    result = parse_document(str(file_path))#解析文档，返回{"full_text":"...","metadata":{...}}
    #在text_splitter.py的split_text函数，将文本切分成块
    chunks = split_text(result["full_text"], chunk_size=500, chunk_overlap=50)

    #将切好的块添加到向量数据库
    add_to_vector_store(
        collection_name=str(current_user.id),
        chunks=chunks,
        file_id=unique_name,
        user_id=current_user.id
    )

    # 保存文档记录到数据库
    existing_doc = db.query(Document).filter(#.query(Document)表示要查询 Document 这张数据库表,.filter(...)添加过滤条件

        Document.file_id == unique_name,
        Document.user_id == current_user.id
    ).first()#返回查询结果的第一条记录(一个 Document 对象)

    #存在则更新,不存在则插入新记录
    if existing_doc:#如果文件已存在,更新原始文件名,文件类型(去掉.的扩展名),文件大小,切块数量
        existing_doc.original_name = file.filename
        existing_doc.file_type = ext[1:]
        existing_doc.file_size = file_size
        existing_doc.chunks_count = len(chunks)
    else:#创建一个新的 Document 对象并加入数据库会话(db.add)
        doc = Document(
            user_id=current_user.id,
            file_id=unique_name,
            original_name=file.filename,
            file_type=ext[1:],
            file_size=file_size,
            chunks_count=len(chunks),
        )
        db.add(doc)
    db.commit()#提交事务,将数据库会话中的所有变更写入数据库

    return {
        "message": "上传成功",
        "file_id": unique_name,
        "original_name": file.filename,
        "file_size": file_size,
        "metadata": result["metadata"],
        "chunks_count": len(chunks),
        "chunks": chunks[:5],
    }

# 问答接口
@app.post("/qa", response_model=QAOut)
async def qa(
    query: str | None = Query(None),
    qa_body: QARequest | None = Body(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    final_query = qa_body.query if qa_body else (query.strip() if query else "")
    if not final_query:
        raise HTTPException(status_code=422, detail="问题不能为空")

    history = [item.model_dump() for item in qa_body.history] if qa_body else []
    api_key = qa_body.api_key if qa_body else None
    api_url = qa_body.api_url if qa_body else None

    result = answer_question(
        user_id=current_user.id,
        query=final_query,
        history=history,
        k=5,
        api_key=api_key,
        api_url=api_url,
    )
    sources_str = "无"

    # 保存问答记录到历史
    try:
        context = result.get("context", [])
        file_ids = list(dict.fromkeys([
            item["metadata"]["file_id"] for item in context
        ]))
        if file_ids:
            docs = db.query(Document).filter(Document.file_id.in_(file_ids)).all()
            sources_str = ", ".join([d.original_name for d in docs])
        else:
            sources_str = "无"

        history = History(
            user_id=current_user.id,
            question=final_query,
            answer=result["answer"],
            sources=sources_str,
        )
        db.add(history)
        db.commit()
    except Exception as e:
        print(f"保存历史记录失败: {e}")

    return {
        "query": final_query,
        "answer": result["answer"],
        "context_count": result["context_count"],
        "sources": sources_str,
    }

# ==================== 文档管理 API ====================

# 获取文档列表
@app.get("/documents", response_model=list[DocumentOut])
def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    docs = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return docs

# 重命名文档
@app.put("/documents/{file_id}", response_model=DocumentOut)
def rename_document(
    file_id: str,
    body: RenameRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    if not body.new_name or not body.new_name.strip():
        raise HTTPException(status_code=422, detail="新文件名不能为空")

    doc = (
        db.query(Document)
        .filter(Document.file_id == file_id, Document.user_id == current_user.id)
        .first()
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="文档不存在")

    doc.original_name = body.new_name.strip()
    db.commit()
    db.refresh(doc)
    return doc

# 删除文档
@app.delete("/documents/{file_id}")
def delete_document(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    doc = (
        db.query(Document)
        .filter(Document.file_id == file_id, Document.user_id == current_user.id)
        .first()
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="文档不存在")

    # 1. 删除物理文件
    file_path = Path("uploads") / str(current_user.id) / file_id
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        print(f"删除文件失败: {e}")

    # 2. 删除向量库中的记录
    try:
        delete_from_vector_store(str(current_user.id), file_id)
    except Exception as e:
        print(f"删除向量记录失败: {e}")

    # 3. 删除数据库记录
    db.delete(doc)
    db.commit()

    return {"message": "删除成功", "file_id": file_id}
# 下载/预览文档
@app.get("/documents/{file_id}/download")
def download_document(
    file_id: str,
    token: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    doc = (
        db.query(Document)
        .filter(Document.file_id == file_id, Document.user_id == current_user.id)
        .first()
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="文档不存在")

    file_path = Path("uploads") / str(current_user.id) / file_id
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    content_type_map = {
        "pdf": "application/pdf",
        "txt": "text/plain; charset=utf-8",
        "md": "text/markdown; charset=utf-8",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    media_type = content_type_map.get(doc.file_type, "application/octet-stream")

    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=doc.original_name,
    )


# ==================== 历史记录 API ====================

# 清空历史记录
@app.delete("/history")
def clear_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    deleted = (
        db.query(History)
        .filter(History.user_id == current_user.id)
        .delete()
    )
    db.commit()
    return {"message": f"已删除 {deleted} 条记录", "count": deleted}

# 获取历史记录列表
@app.get("/history", response_model=list[HistoryOut])
def list_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    records = (
        db.query(History)
        .filter(History.user_id == current_user.id)
        .order_by(History.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return records

# 获取单条历史记录详情
@app.get("/history/{history_id}", response_model=HistoryOut)
def get_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    api_key: str = None,
    api_url: str = None,
):
    record = (
        db.query(History)
        .filter(History.id == history_id, History.user_id == current_user.id)
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record


# ==================== 异常处理 ====================

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=404,
            content={"detail": "请求的资源不存在", "status_code": 404},
        )
    if exc.status_code == status.HTTP_403_FORBIDDEN:
        return JSONResponse(
            status_code=403,
            content={"detail": "无权限访问", "status_code": 403},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail), "status_code": exc.status_code},
    )
