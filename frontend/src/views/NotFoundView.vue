<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const homePath = computed(() => (localStorage.getItem('token') ? '/knowledge' : '/login'))

function goHome() {
  router.push(homePath.value)
}
</script>

<template>
  <div class="status-page">
    <div class="status-card">
      <span class="status-code">404</span>
      <h1>页面不存在</h1>
      <p>你访问的页面不存在，可能是地址输入错误，或者页面已经被移动。</p>
      <div class="actions">
        <button class="primary-btn" @click="goHome">返回首页</button>
        <button class="ghost-btn" @click="router.back()">返回上一页</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.status-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: var(--brand-blue);
}

.status-card {
  width: min(520px, 100%);
  padding: 32px;
  border: 4px solid #000000;
  box-shadow: 8px 8px 0 #000000;
  background: #FFFFFF;
  text-align: center;
}

.status-code {
  display: inline-block;
  margin-bottom: 12px;
  padding: 6px 12px;
  border: 3px solid #000000;
  background: #F0C050;
  color: #000000;
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 900;
  letter-spacing: 4px;
}

h1 {
  margin: 0;
  font-family: "Arial Black", "Impact", sans-serif;
  font-size: 32px;
  letter-spacing: 4px;
}

p {
  margin: 16px 0 0;
  font-family: var(--font-family);
  font-size: 15px;
  font-weight: 700;
  line-height: 1.6;
  color: var(--text-muted);
}

.actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

button {
  padding: 10px 18px;
  border: 2px solid #000000;
  box-shadow: 3px 3px 0 #000000;
  cursor: pointer;
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 900;
  text-transform: uppercase;
}

.primary-btn {
  background: var(--brand-blue);
  color: #FFFFFF;
}

.ghost-btn {
  background: var(--brand-coral);
  color: #FFFFFF;
}

button:hover {
  transform: translate(2px, 2px);
  box-shadow: 1px 1px 0 #000000;
}
</style>
