import os
from dotenv import load_dotenv
import requests
from services.vector_store import search_vector_store

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def build_prompt(query: str, context: list) -> str:
    context_text = "\n\n".join([item["text"] for item in context])
    prompt = f"""你是一个智能文档助手，根据提供的文档内容回答问题。

文档内容：
{context_text}

问题：{query}

请根据文档内容回答问题。如果文档中没有相关信息，请回答"文档中没有相关信息"。
"""
    return prompt.strip()

def call_deepseek(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-v4-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API调用失败: {str(e)}"

def answer_question(user_id: int, query: str, k: int = 5) -> dict:
    context = search_vector_store(str(user_id), query, k=k)
    if not context:
        return {"answer": "文档中没有相关信息", "context_count": 0, "context": []}
    prompt = build_prompt(query, context)
    answer = call_deepseek(prompt)
    return {"answer": answer, "context_count": len(context), "context": context}
