import { defineStore } from 'pinia'
import { ref } from 'vue'

interface User {//给对象写一份"规格说明书"
  id: number
  email: string
  username: string
}

//定义一个叫auth的store,存储用户认证相关的信息(由pinia管理)
export const useAuthStore = defineStore('auth', () => {

	//ref让它变成 响应式 ——当值变化时，所有用到它的组件都会自动更新
	const token = ref<string | null>(localStorage.getItem('token'))// 从localStorage中获取token,如果不存在则为null
	const user = ref<User | null>(null)
	const loading = ref(false)

	//使用: auth.setToken('xxx')  // 写入 token
  function setToken(newToken: string) {
    token.value = newToken// 设置token为新token
    localStorage.setItem('token', newToken)// 将新token存储到localStorage中
  }

  const signature=ref<string>(localStorage.getItem('signature')||'just do it')
  function setSignature(val:string){
    signature.value=val
    localStorage.setItem('signature', val)
  }
  //使用: auth.logout()  // 清除 token
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')// 从localStorage中删除token
  }

  return { token, user, loading, setToken, logout, signature, setSignature }
})
