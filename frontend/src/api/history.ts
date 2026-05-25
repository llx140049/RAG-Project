import apiClient from './client'

export interface HistoryItem {
    id: number
    question: string
    answer: string
    sources: string|null//来源
    created_at: string//创建时间
}

export function getHistoryList(skip=0, limit=10) {
    return apiClient.get<HistoryItem[]>('/history', { params: { skip, limit } })
}

export function getHistoryDetail(id: number) {
    return apiClient.get<HistoryItem>(`/history/${id}`)
}
export function deleteHistory() {
    return apiClient.delete('/history')
}
