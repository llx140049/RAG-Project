<script setup lang="ts">
import { onMounted } from 'vue'
import { useHistoryStore } from '../stores/history'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useHistoryStore()

async function handleClear() {
  try {
    await ElMessageBox.confirm('确定清空所有历史记录？', '清空确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await store.clearHistory()
    ElMessage.success('已清空')
  } catch (e: any) {
    if (e !== 'cancel') ElMessage.error('清空失败')
  }
}

function formatDate(iso: string) {
  const d = new Date(iso)
  const y = d.getFullYear()
  const mo = d.getMonth() + 1
  const day = d.getDate()
  const h = String(d.getHours()).padStart(2, '0')
  const mi = String(d.getMinutes()).padStart(2, '0')
  return `${y}-${mo}-${day} ${h}:${mi}`
}

onMounted(() => store.loadHistory())
</script>

<template>
  <div class="history-page">
    <header class="page-header">
<div class="header-left">
        <h1>历史记录</h1>
        <p>浏览过往问答</p>
      </div>
      <button class="clear-btn" @click="handleClear">清空记录</button>
    </header>

    <div class="table-card">
      <el-table
        :data="store.records"
        v-loading="store.loading"
        stripe
        style="width: 100%"
      >
        <el-table-column type="expand">
          <template #default="{ row }">
            <div class="expand-body">
              <div class="expand-question">
                <span class="expand-label">Q</span>
                <p>{{ (row as any).question }}</p>
              </div>
              <div class="expand-answer">
                <span class="expand-label">A</span>
                <p>{{ (row as any).answer }}</p>
              </div>
              <div class="expand-meta">
                <span>来源：{{ (row as any).sources || '无' }}</span>               
                <span>时间：{{ formatDate((row as any).created_at) }}</span>

              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="question" label="问题" min-width="280" show-overflow-tooltip />

        <el-table-column label="回答概要" min-width="320">
          <template #default="{ row }">
            {{ (row as any).answer?.slice(0, 80) + '...' }}
          </template>
        </el-table-column>
        
        <el-table-column label="来源" min-width="160" align="center">
          <template #default="{ row }">
            {{ (row as any).sources || '无' }}
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style scoped>
.history-page {
  display: flex;
  position: relative;
  flex-direction: column;
  width: 100%;
  min-height: 100%;/*父元素高度增加时能随之增加*/
  padding: 24px 32px;
  background: var(--brand-blue);
}

.history-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255, 255, 255, 0.123) 39px, rgba(255,255,255,0.123) 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,255,255,0.123) 39px, rgba(255,255,255,0.123) 40px);
  pointer-events: none;
  z-index: 0;
}

.page-header {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  background-color: #F0C050;
  border: 3px solid #000000;
  box-shadow: 5px 5px 0px #000000;
  padding: 8px 25px;
  margin-bottom: 20px;
}
.header-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px;
}

.page-header h1 {
  font-family: "Arial Black", "Impact", sans-serif;
  font-size: 28px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 6px;
  margin: 0 20px 0 0;
}

.page-header p {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  margin: 0;
}
.clear-btn {
  font-family: var(--font-mono);
  font-size: 15px;
  font-weight: 900;
  color: #FFFFFF;
  text-transform: uppercase;
  background: var(--brand-blue);
  border: 2px solid #000;
  box-shadow: 3px 3px 0px #000;
  cursor: pointer;
  padding: 10px 20px;
  transition: transform 0.1s, box-shadow 0.1s;
}
.clear-btn:hover {
  transform: translate(2px, 2px);
  box-shadow: 1px 1px 0px #000;
}
.clear-btn:active {
  transform: translate(3px, 3px);
  box-shadow: none;
}


.table-card {
  position: relative;
  z-index: 1;
  border: 3px solid #000000;
  box-shadow: 5px 5px 0px #000000;
  background: #FFFFFF;
}

/* ===== Expand area ===== */
.expand-body {
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.expand-question,
.expand-answer {
  display: flex;
  gap: 12px;
  padding: 14px 16px;
}

.expand-question {
  background: var(--brand-gold);
  border: 2px solid #000;
  border-bottom: none;
}

.expand-answer {
  background: #FFF;
  border: 2px solid #000;
  border-left: 5px solid var(--brand-coral);
  border-top: none;
}

.expand-label {
  font-family: var(--font-mono);
  font-size: 18px;
  font-weight: 900;
  width: 32px;
  height: 32px;
  border: 2px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: #FFF;
}

.expand-question p,
.expand-answer p {
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 700;
  line-height: 1.6;
  color: var(--text-primary);
  margin: 0;
  white-space: pre-wrap;
  flex: 1;
}

.expand-meta {
  display: flex;
  gap: 24px;
  padding: 10px 16px;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  background: #FAFAFA;
  border: 2px solid #000;
  border-top: none;
}
</style>
