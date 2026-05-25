from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

#SQLAlchemy 连接 SQLite 数据库的标准初始化三步曲
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rag.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):#SQLAlchemy 会扫描所有继承 Base 的类，自动创建对应的数据库表
    pass

# 数据库会话依赖项
def get_db():
    db = SessionLocal()# 创建数据库会话
    # 确保数据库会话在请求处理完成后关闭，避免资源泄漏
    try:# 尝试获取数据库会话
        yield db# 返回数据库会话,路由函数执行完后，代码 回到 yield 的下一行 继续执行
    finally:# 无论是否发生异常，都关闭数据库会话
        db.close()
