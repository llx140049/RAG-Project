def split_text(text: str, chunk_size: int = 250, chunk_overlap: int = 50) -> list:
    
    #初始化变量
    chunks = []#结果列表[{"chunk_id":0,"text":"...","length":0},...]
    start = 0#当前块的起始位置
    text_length = len(text)#文本总长度(不变)
    
    while start < text_length:
        end = start + chunk_size
        
        # 如果不是最后一块，尝试在合适的位置断开
        if end < text_length:
            chunk = text[start:end]#取当前候选块
            
            # 优先在段落或句子边界处断开
            separators = ["\n\n", "\n", "\r\n", "。", "！", "？", ".", "!", "?", "；", ";", "，", ","]
            for sep in separators:
                idx = chunk.rfind(sep)#从右往左找分隔符,如果找到,返回它的索引,如果没有找到,返回-1                                                                                                                                                                                                       
                if idx != -1 and idx > chunk_size // 2:#分隔符在块的后半
                    end = start + idx + len(sep)#在分隔符后断开
                    break
        
        chunk_text = text[start:end]#根据调整后的 end 取文本
        
        if chunk_text.strip():#如果这块文本去掉空白后不是空的，才保存
            chunks.append({#.append() — 列表方法，在列表末尾添加一个元素
                "chunk_id": len(chunks),
                "text": chunk_text.strip(),
                "length": len(chunk_text.strip())
            })
        
        # 移动到下一个块，考虑重叠
        start = end - chunk_overlap
        
        # 防止无限循环
        if start >= text_length:
            break
    
    return chunks
