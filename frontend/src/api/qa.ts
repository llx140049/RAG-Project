import apiClient from './client'

export interface QAResponse {
  query: string
  answer: string
  context_count: number
  sources?: string
}

// 提交问题
export function askQuestion(query: string) {
  return apiClient.post<QAResponse>('/qa', null, { params: { query } })
}
