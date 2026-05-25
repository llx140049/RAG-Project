<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { ElMessage } from 'element-plus'
import apiClient from '../api/client'

const router = useRouter()
const authStore = useAuthStore()
const activeTab = ref<'login' | 'register'>('login')
const loading = ref(false)

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ email: '', username: '', password: '' })

async function handleLogin() {
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('username', loginForm.username)
    formData.append('password', loginForm.password)
    const res = await apiClient.post('/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    authStore.setToken(res.data.access_token)
    router.push('/knowledge')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  loading.value = true
  try {
    await apiClient.post('/register', registerForm)
    ElMessage.success('注册成功，请登录')
    activeTab.value = 'login'
    loginForm.username = registerForm.username
    loginForm.password = ''
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <div class="brand-panel">
        <img class="logo" src="/assets/logo.svg" alt="LCRAG logo" width="170" height="170" />
        <h2>LCRAG</h2>
        <p class="subtitle">knowledge workspace</p>
      </div>

      <div class="form-panel">
        <el-tabs v-model="activeTab" class="auth-tabs">
          <el-tab-pane label="登录" name="login">
            <el-form @submit.prevent="handleLogin" label-position="top">
              <el-form-item label="用户名">
                <el-input v-model="loginForm.username" size="large" />
              </el-form-item>
              <el-form-item label="密码">
                <el-input v-model="loginForm.password" type="password" size="large" show-password />
              </el-form-item>
              <el-button type="primary" size="large" :loading="loading" native-type="submit" >
                登录
              </el-button>
            </el-form>
          </el-tab-pane>

          <el-tab-pane label="注册" name="register">
            <el-form @submit.prevent="handleRegister" label-position="top">
              <el-form-item label="邮箱">
                <el-input v-model="registerForm.email" size="large" />
              </el-form-item>
              <el-form-item label="用户名">
                <el-input v-model="registerForm.username" size="large" />
              </el-form-item>
              <el-form-item label="密码">
                <el-input v-model="registerForm.password" type="password" size="large" show-password />
              </el-form-item>
              <el-button type="primary" size="large" :loading="loading" native-type="submit" >
                注册
              </el-button>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-cream);
   }

.login-container {
  display: flex;
  background: #FFFFFF;
  border: var(--border-width) solid var(--border-warm);
	border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  max-width: 700px;
  width: 100%;
  overflow: hidden;/*裁切子元素,防止父圆子方*/
}

.brand-panel {
  width: 270px;
  padding: 15px 36px 56px 36px;
  background: var(--bg-sidebar);
  border-right: var(--border-width) solid var(--border-warm);
  display: flex;
  flex-direction: column;/* 垂直方向 */
  align-items: center;
	justify-content: center;
}

.brand-panel .logo { margin-bottom: -30px; }
.brand-panel h2 {
  font-size: 45px;
  font-weight: 900;/* 加粗 */
	font-family: var(--font-family);
  color: var(--text-primary);
  text-transform: uppercase;/* 大写 */
  letter-spacing: 3px;/* 字间距 */

}
/*副标题 */
.subtitle {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-muted);
  font-family: var(--font-mono);
	
  margin-top: 4px;
  text-transform: lowercase;
}
/* 登录注册表单 */
.form-panel {
  flex: 1;
  padding: 45px 45px;/* 内边距 */
  display: flex;
  align-items: center;
  background: var(--brand-blue);
  }

.auth-tabs { 
	width: 95%; 
	overflow: visible;
} 

.auth-tabs :deep(.el-tabs__content) {
	overflow: visible;/*防止剪裁shadow*/
}

.auth-tabs :deep(.el-tabs__nav-wrap) {
	overflow: visible;
}

.auth-tabs :deep(.el-tabs__header) {
  border-bottom: var(--border-width) solid var(--border-warm);
  margin-bottom: 23px;
}

.auth-tabs :deep(.el-tabs__item) {
  font-family: var(--font-mono);
  font-weight: 1000 !important;
  font-size: 18px;
  text-transform: uppercase;
  letter-spacing: 2px;
}
/* 登录注册表单标签 */
.auth-tabs :deep(.el-form-item__label) {
  font-family: var(--font-mono);
  font-weight: 1000 !important;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.auth-tabs :deep(.el-input__wrapper) {
  border: 2px solid var(--border-warm) !important;
  box-shadow: 5px 5px 0px var(--border-warm) !important;
  border-radius: var(--border-radius) !important;
  font-weight: 700 !important;
  }
/* 登录注册按钮 */
.auth-tabs :deep(.el-button--primary) {
	display: block;/*把 Element Plus 按钮变成块级元素*/
	width: 50% !important;
	margin: 0 auto;/*居中*/
  font-family: var(--font-mono);
  font-weight: 1000 !important;
  letter-spacing: 5px;
  border: 2px solid var(--border-warm) !important;
  box-shadow: 6px 6px 0px var(--border-warm) !important;
  border-radius: var(--border-radius) !important;
  transition: transform 0.1s, box-shadow 0.1s !important;
}

.auth-tabs :deep(.el-button--primary:hover) {
	background-color: var(--brand-gold) !important;
	color: var(--text-primary) !important;
	transform: translate(2px, 2px) !important;
	box-shadow: 4px 4px 0px var(--border-warm) !important;
}
.auth-tabs :deep(.el-button--primary:active) {
	transform: translate(3px, 3px) !important;
	box-shadow: none !important;
}

</style>
