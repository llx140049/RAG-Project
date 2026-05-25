import apiClient from "./client"

export interface DocumentItem {
    id: number
    file_id: string
    original_name: string
    file_type: string
    file_size: number
    chunks_count: number
    created_at: string
}

// 获取文档列表
export function fetchDocuments(skip=0,limit=20) {
    //发送一个 HTTP GET 请求到 /documents 路径,
    //<DocumentItem[]>告诉 TS 返回的响应体是 DocumentItem 数组
    //URL 查询参数,最终请求 URL 类似于 /documents?skip=0&limit=20
    return apiClient.get<DocumentItem[]>('/documents',{params:{skip,limit}})
}

// 更新文档名称
export function renameDocument(fileId:string,newName:string) {
    return apiClient.put<DocumentItem>(`/documents/${fileId}`,
        {new_name: newName})
}

// 删除文档
export function deleteDocument(fileId:string) {
    return apiClient.delete(`/documents/${fileId}`)
}

//上传文件
export function uploadDocument(file:File) {
    const formData=new FormData()
    formData.append('file',file)
    return apiClient.post('/upload',formData,{headers:{'Content-Type': 'multipart/form-data'}})
        
}