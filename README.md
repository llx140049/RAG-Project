﻿# 🚀 RAG-Project 🚀

基于 RAG 架构的智能文档问答系统。上传文档后，系统自动解析、向量化存储，支持对文档内容进行自然语言提问，由 LLM 结合检索到的上下文生成精准回答。

## ✨ 功能特性

- 🔐 **用户认证** — JWT 令牌登录/注册，多用户隔离
- 📄 **文档管理** — 支持 PDF、DOCX、TXT、Markdown 文件，上传/下载/预览/重命名/删除
- ✂️ **智能切块** — 自动文本分割，带重叠窗口，优先在段落/句子边界断开
- 🔍 **向量检索** — ChromaDB + BGE 中文嵌入模型，语义检索相关内容
- 💬 **文档问答** — 检索 + DeepSeek 大模型生成回答，返回引用来源
- 🕐 **历史记录** — 问答历史持久化存储，支持查看和清空

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 🌐 后端框架 | FastAPI + Uvicorn |
| 🗄️ 数据库 | SQLite + SQLAlchemy ORM |
| 🧬 向量数据库 | ChromaDB |
| 🧠 嵌入模型 | BAAI/bge-small-zh-v1.5 |
| 📑 文档解析 | PyPDF2 / python-docx |
| 🤖 LLM | DeepSeek API (deepseek-v4-flash) |
| 🎨 前端框架 | Vue 3 + TypeScript + Vite |
| 🧩 UI 组件库 | Element Plus |
| 📦 状态管理 | Pinia |

## 📁 项目结构

```
RAG-Project/
  main.py                  # FastAPI 入口，路由 & 中间件
  models.py                # SQLAlchemy 数据模型（User/Document/History）
  schemas.py               # Pydantic 请求/响应模型
  database.py              # 数据库引擎 & 会话管理
  requirements.txt         # Python 依赖
  .env.example             # 环境变量模板
  services/
      document_parser.py   # 文档解析（PDF/DOCX/TXT/MD）
      text_splitter.py     # 文本分块 & 重叠窗口
      vector_store.py      # ChromaDB 向量存储 & 检索
      qa_service.py        # RAG 问答服务（DeepSeek）
  frontend/                # Vue 3 前端
      src/
          views/           # 页面组件
          stores/          # Pinia 状态
          api/             # Axios 请求封装
          router/          # Vue Router
      package.json
  assets/                  # 设计稿 / UI  原型
```



## 🏃 快速开始

#### 📋 环境要求

- Python 3.10+
- Node.js 18+
- HuggingFace 本地模型缓存（BAAI/bge-small-zh-v1.5）

### 📥 1. 克隆项目

```bash
git clone <your-repo-url>
cd RAG-Project
```

### 🔧 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 .env 文件，填入你的密钥：

```env
JWT_SECRET=your-secret-key
DATABASE_URL=sqlite:///./rag.db
DEEPSEEK_API_KEY=your-deepseek-api-key
```

### ⚙️ 3. 安装后端依赖 & 启动

```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 启动后端（默认 http://localhost:8000）
uvicorn main:app --reload
```

### 🎨 4. 安装前端依赖 & 启动

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器默认运行在 http://localhost:5173。

### 🧠 5. 下载嵌入模型（首次使用）

项目使用 BAAI/bge-small-zh-v1.5 作为嵌入模型。首次运行前需本地缓存：

```bash
huggingface-cli download BAAI/bge-small-zh-v1.5
```

或通过 Python：

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
```

## 📡 API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /register | 用户注册 |
| POST | /login | 用户登录 |
| GET | /me | 获取当前用户信息 |
| POST | /upload | 上传文档 |
| GET | /documents | 文档列表 |
| PATCH | /documents/{file_id}/rename | 重命名文档 |
| DELETE | /documents/{file_id} | 删除文档 |
| GET | /documents/{file_id}/download | 下载/预览文档 |
| POST | /qa | 文档问答 |
| GET | /history | 历史记录列表 |
| GET | /history/{history_id} | 单条历史详情 |
| DELETE | /history | 清空历史 |

## 🤖 AI 开发使用情况

本项目在开发过程中使用了 AI 辅助编程工具，以下为使用详情。

| 工具/平台 | 用途 | 说明 |
|-----------|------|------|
| Trae /  Codex | 代码生成与补全 | 生成后端 API 路由、数据模型、服务逻辑等 Python 代码 |
| Trae/ Codex | 前端脚手架与页面 | 辅助生成 Vue 3 组件、路由、状态管理、API 客户端等前端代码 |
| AI 辅助调试 | Bug 修复 | 协助排查逻辑错误、修正中文编码与类型问题 |



## 📜 License

MIT
