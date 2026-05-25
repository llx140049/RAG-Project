from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

# 用户注册请求模型
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) < 2:
            raise ValueError("用户名至少需要 2 个字符")
        if len(v) > 32:
            raise ValueError("用户名不能超过 32 个字符")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 4:
            raise ValueError("密码至少需要 4 个字符")
        if len(v) > 128:
            raise ValueError("密码不能超过 128 个字符")
        return v

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
