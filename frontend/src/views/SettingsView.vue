<script setup lang="ts">

import { ref } from "vue"
import { useAuthStore } from "../stores/auth"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"

const auth = useAuthStore()
const router = useRouter()
const sigInput = ref(auth.signature)
const modelURL = ref(localStorage.getItem("model-url") || "")
const modelKey = ref(localStorage.getItem("model-key") || "")
const modelKeyVisible = ref(false)

function saveSignature() {
  auth.setSignature(sigInput.value)
  ElMessage.success("签名已保存")
}
function saveModel() {
  localStorage.setItem("model-url", modelURL.value)
  localStorage.setItem("model-key", modelKey.value)
  ElMessage.success("模型配置已保存")
}
function doLogout() {
  auth.logout()
  router.push("/login")
}

</script>

<template>
  <div class="settings-page grid-page">
    <span class="page-label">SETTINGS</span>

    <div class="settings-grid">
      <!-- 签名 -->
      <section class="card signature-card">
        <h3 class="card-title">
          <span class="icon-block icon-gold"></span> 签名
        </h3>
        <div class="input-group">
          <label class="input-label">个性签名</label>
          <el-input
            v-model="sigInput"
            placeholder="输入签名…"
            clearable
            size="large"
          />
        </div>
        <el-button class="btn-save" @click="saveSignature" size="large">
          保存
        </el-button>
        
      </section>

      <!-- 模型配置 -->
      <section class="card model-card">
        <h3 class="card-title">
          <span class="icon-block icon-coral"></span> 模型配置
        </h3>
        <div class="input-group">
          <label class="input-label">API URL</label>
          <el-input
            v-model="modelURL"
            placeholder="https://api.openai.com/v1"
            clearable
            size="large"
          />
        </div>
        <div class="input-group">
          <label class="input-label">API Key</label>
          <div class="input-wrapper">
            <el-input
              v-model="modelKey"
              placeholder="sk-················"
              clearable
              size="large"
              :type="modelKeyVisible ? 'text' : 'password'"
            />
            <button
              class="toggle-vis"
              type="button"
              @click="modelKeyVisible = !modelKeyVisible"
            >
              {{ modelKeyVisible ? "隐" : "显" }}
            </button>
          </div>
        </div>
        <el-button class="btn-save" @click="saveModel" size="large">
          保存
        </el-button>
      </section>

      <!-- 退出登录 -->
      <section class="card logout-card">
        
        <el-button class="btn-danger" @click="doLogout" size="large">
          退出登录
        </el-button>
      </section>
    </div>
  </div>
</template>

<style scoped>
.settings-page {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.page-label {
  position: absolute;
  top: 24px;
  left: 40px;
  font-size: 35px;
  font-weight: 900;
  color: #fff;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-shadow: 3px 3px 0px #000000;
  z-index: 1;/* 确保标签在卡片之上 */

}

.settings-grid {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: center;
  gap: 32px;
  padding: 60px 40px 40px;
  max-width: 1100px;
  width: 100%;
  z-index: 1;
}

/* ===== Cards ===== */
.card {
  background: #FFFFFF;
  border: 3px solid #000000;
  box-shadow: 5px 5px 0px #000;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: transform 0.15s, box-shadow 0.15s;
}
.card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 7px 7px 0px #000;
}

.signature-card { width: 460px; }
.model-card { width: 460px; }
.logout-card {
  width: 280px;
  align-self: stretch;
  justify-content: space-between;
}

.card-title {
  font-size: 18px;
  font-weight: 900;
  color: var(--text-primary);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 8px;
  border-bottom: 3px solid #000;
}

.icon-block {
  width: 28px;
  height: 28px;
  border: 2px solid #000;
  flex-shrink: 0;
}
.icon-gold { background: var(--brand-gold); }
.icon-coral { background: var(--brand-coral); }
.icon-red { background: #DC2626; }

/* ===== Input ===== */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.input-label {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
}

.input-wrapper {
  position: relative;
}
/* */
.toggle-vis {
  position: absolute;
  right: 4px;
  top: 4px;
  bottom: 4px;
  width: 42px;
  background: #f0f0f0;
  border: 2px solid #000;
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ===== Buttons ===== */
.btn-save {
  align-self: flex-start;
  background: var(--brand-blue) !important;
  color: #fff !important;
  font-weight: 800 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-danger {
  width: 100%;
  background: #DC2626 !important;
  color: #fff !important;
  font-weight: 800 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.logout-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
}

/**/
.settings-page :deep(.el-input__wrapper) {
  border: 2px solid #000 !important;
  border-radius: 0 !important;
  box-shadow: 3px 3px 0px #000 !important;
  font-family: var(--font-mono);
  font-weight: 700;
}
.settings-page :deep(.el-input.is-focus .el-input__wrapper) {
  background: #FFF9E6 !important;
  box-shadow: 4px 4px 0px #000 !important;
  transform: translate(-1px, -1px);
}
.settings-page :deep(.el-input__inner) {
  font-family: var(--font-mono) !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
}
.settings-page :deep(.el-input__inner::placeholder) {
  color: #aaa !important;
  font-weight: 400 !important;
  font-style: italic !important;
}

.settings-page :deep(.el-button) {
  border-radius: 0 !important;
  border: 2px solid #000 !important;
  box-shadow: 3px 3px 0px #000 !important;
  font-weight: 800;
  transition: transform 0.1s, box-shadow 0.1s;
}
.settings-page :deep(.el-button:hover) {
  transform: translate(2px, 2px);
  box-shadow: 1px 1px 0px #000 !important;
}
.settings-page :deep(.el-button:active) {
  transform: translate(3px, 3px);
  box-shadow: none !important;
}

/* API Key 输入框给右侧 toggle 留空间 */
.input-wrapper :deep(.el-input__wrapper) {
  padding-right: 50px !important;
}
</style>
