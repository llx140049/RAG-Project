import os
from dotenv import load_dotenv
import requests
from services.vector_store import search_vector_store

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def build_prompt(query: str, context: list) -> str:
    context_text = "\n\n".join([item["text"] for item in context])
    prompt = f"""你是产品中的智能助手，正在和用户进行自然对话。

文档内容：
{context_text}

问题：{query}

回答要求：
1. 先判断用户问题属于哪一类：
   - 如果是在询问文档、知识库、学习内容、项目内容、资料总结，优先基于给定文档回答。
   - 如果明显是在闲聊、安慰、讲笑话、日常聊天、开放式陪伴，不要被文档限制，可以像正常助手一样直接回答。
2. 只有当用户明确在问文档内容，而文档中又确实没有相关信息时，才回答“文档中没有相关信息”。
3. 不要把“文档里没有提到”机械地用在闲聊类问题上。比如用户让你讲笑话、安慰他、闲聊时，直接正常回答即可。
4. 回答要像正常助手在聊天，语气自然、直接、简洁，不要像检索报告或论文总结。
5. 不要使用 Markdown 语法，不要输出 **加粗**、# 标题、代码块，也不要使用刻意的编号列表。
6. 优先用 2 到 4 句话回答；先直接回答用户问题，再补充一点必要说明。
7. 当用户问“主要内容是什么”“学到了什么”“可以分成哪些大类”这类总结题时，可以根据文档内容直接归纳，不要先否定再回答。
8. 尽量少说“根据您提供的文档内容”“文档里没有明确提到”这类生硬套话。能自然回答就直接回答。
9. 如果需要分类，使用自然表达，例如“从这些资料来看，大致可以分为……”。不要写成生硬条目清单。
10. 不要重复用户问题，不要写开场寒暄，不要加多余免责声明。
11. 让回答读起来像产品里的助手消息，而不是文档摘要器。
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
