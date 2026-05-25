import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"#国内镜像加速
os.environ["HF_HUB_OFFLINE"] = "1"#不连接 HuggingFace 检查更新
os.environ["TRANSFORMERS_OFFLINE"] = "1"#不尝试联网下载，只用本地缓存

# 全局嵌入模型实例
_embedding_model = None
_EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"


def _resolve_local_model_path(model_name: str) -> str:
    """优先使用本地 HuggingFace snapshot，避免加载时触发联网探测。"""
    cache_root = Path.home() / ".cache" / "huggingface" / "hub"
    repo_dir = cache_root / f"models--{model_name.replace('/', '--')}"
    snapshots_dir = repo_dir / "snapshots"

    if snapshots_dir.exists():
        snapshots = sorted([p for p in snapshots_dir.iterdir() if p.is_dir()])
        if snapshots:
            return str(snapshots[-1])
    return model_name

#模型懒加载
def get_embeddings():
    #获取嵌入模型（中英文支持）
    global _embedding_model# 
    if _embedding_model is None:#第二次调用 get_embeddings(): _embedding_model 不是 None → 直接返回，0 秒等待
        model_source = _resolve_local_model_path(_EMBEDDING_MODEL_NAME)
        try:
            _embedding_model = SentenceTransformer(
                model_source,
                local_files_only=True,
                trust_remote_code=False,
            )
        except Exception as exc:
            raise RuntimeError(
                f"本地嵌入模型加载失败: {model_source}。请检查 HuggingFace 缓存是否完整。"
            ) from exc
    return _embedding_model#整个应用生命周期中，模型只加载一次

#PersistentClient 把数据存到磁盘上的 chroma_db/ 目录里，每次启动应用时都从这里读取
def get_chroma_client():
    """初始化 Chroma 客户端"""
    return chromadb.PersistentClient(path="./chroma_db")

#获取或创建向量数据库集合
def get_vector_store(collection_name: str):
    
    client = get_chroma_client()
    
    # Chroma 集合名称要求：3-512字符，只包含 [a-zA-Z0-9._-]，以字母或数字开头和结尾
    if len(collection_name) < 3:
        collection_name = f"user_{collection_name}"#长度小于3,加上_user前缀
    
    return client.get_or_create_collection(name=collection_name)#幂等操作

#添加文档到向量数据库
def add_to_vector_store(collection_name: str, chunks: list, file_id: str, user_id: int):
    
    collection = get_vector_store(collection_name)
    model = get_embeddings()
    
    texts = [chunk["text"] for chunk in chunks]#过滤出chunks的每个chunk的text部分,组成一个列表
    # 生成每个chunk的id,格式为 file_id_chunk_i
    ids = [f"{file_id}_chunk_{i}" for i in range(len(chunks))]
    #生成元数据（文件ID、块序号、块长度、用户ID）
    metadatas = [
        {"file_id": file_id, "chunk_id": i, "length": chunk["length"], "user_id": user_id}
        for i, chunk in enumerate(chunks)
    ]
    
    # 生成向量
    embeddings = model.encode(texts).tolist()
    
    # 添加到集合
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    return len(chunks)

 #从向量数据库检索相关内容
def search_vector_store(collection_name: str, query: str, k: int = 5):
    
    collection = get_vector_store(collection_name)#获取集合
    model = get_embeddings()
    
    # 生成查询向量,将用户的自然语言查询通过嵌入模型转换为一个 语义向量
    query_embedding = model.encode(query).tolist()
    
    # 执行检索
    results = collection.query(
        query_embeddings=[query_embedding],#查询向量列表，这里只有一个元素，就是 query_embedding
        n_results=k,#返回的结果数量
        include=["documents", "metadatas"]#返回文档和元数据
    )
    
    # 整理结果格式
    return [
        {"text": results["documents"][0][i], "metadata": results["metadatas"][0][i]}
        for i in range(len(results["documents"][0]))
    ]


def delete_from_vector_store(collection_name: str, file_id: str):
    """
    删除指定文件的所有向量
    
    Args:
        collection_name: 集合名称
        file_id: 文件ID
    
    Returns:
        删除的数量
    """
    collection = get_vector_store(collection_name)
    
    # 查询该文件的所有块
    results = collection.get(
        where={"file_id": file_id},
        include=[]
    )
    
    if results["ids"]:
        collection.delete(ids=results["ids"])
        return len(results["ids"])
    return 0

