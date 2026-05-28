import apiClient from './client'

export interface QAResponse {
  query: string
  answer: string
  context_count: number
  sources?: string
}

export interface ChatMessagePayload {
  role: 'user' | 'assistant'
  content: string
}

export interface QARequestPayload {
  query: string
  history?: ChatMessagePayload[]
  apiKey?: string
  apiUrl?: string
}

// 提交问题
export function askQuestion(payload: QARequestPayload) {
  return apiClient.post<QAResponse>('/qa', {
    query: payload.query,
    history: payload.history ?? [],
    api_key: payload.apiKey,
    api_url: payload.apiUrl,
  })
}
