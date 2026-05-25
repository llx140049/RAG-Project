from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 用户注册请求模型
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

# 用户注册响应模型
class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True

# 用户登录响应模型
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 文档输出模型
class DocumentOut(BaseModel):
    id: int
    file_id: str
    original_name: str
    file_type: str
    file_size: int
    chunks_count: int
    created_at: datetime

    class Config:
        from_attributes = True

# 文档重命名请求模型
class RenameRequest(BaseModel):
    new_name: str

# 历史记录输出模型
class HistoryOut(BaseModel):
    id: int
    question: str
    answer: str
    sources: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class QAOut(BaseModel):
    query: str
    answer: str
    context_count: int
    sources: Optional[str] = None
