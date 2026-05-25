import axios from 'axios'
//Axios 是前端最流行的 HTTP 请求库 。它的作用是让浏览器和服务器之间 发送/接收数据 。

const apiClient = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
})

//请求拦截器（请求发出前自动执行,自动带 token）
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

//响应拦截器（收到响应后自动执行,自动处理 401 错误）
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else if (err.response?.status === 403) {
      window.location.href = '/403'
    }
    return Promise.reject(err)
  }
)

export default apiClient
