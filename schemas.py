from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Literal, Optional

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


class ChatMessageIn(BaseModel):
    role: Literal["user", "assistant"]
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("消息内容不能为空")
        return v


class QARequest(BaseModel):
    query: str
    history: list[ChatMessageIn] = Field(default_factory=list)
    api_key: Optional[str] = None
    api_url: Optional[str] = None

    @field_validator("query")
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("问题不能为空")
        return v


class QAOut(BaseModel):
    query: str
    answer: str
    context_count: int
    sources: Optional[str] = None
