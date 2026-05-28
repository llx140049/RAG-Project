<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useHistoryStore } from '../stores/history'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDateTime } from '../utils/format'

const store = useHistoryStore()//获取历史记录存储实例
const page = ref(1)
const pageSize = 6

// 切分历史记录列表,6条/页
const pageRecords = computed(() => {
  const start = (page.value - 1) * pageSize
  return store.records.slice(start, start + pageSize)
})

watch(// 监听历史记录列表长度变化->执行更新分页
  () => store.records.length,
  (length) => {
    const maxPage = Math.max(1, Math.ceil(length / pageSize))
    if (page.value > maxPage) page.value = maxPage
  }
)

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
    if (e !== 'cancel') ElMessage.error('清空失败')//如果用户点击了取消,则不显示错误提示
  }
}

onMounted(() => store.loadHistory(0, 100))
</script>

<template>
  <div class="history-page grid-page">
    <header class="page-header">
      <div class="header-left">
        <h1>历史记录</h1>
        <p>浏览过往问答</p>
      </div>
      <button class="clear-btn" @click="handleClear">清空记录</button>
    </header>

    <!--:data="store.records" : 把 store.records 作为表格的数据源传给 el-table-->
    <div class="table-card">
      <el-table
        :data="pageRecords"
        v-loading="store.loading"
        stripe
        style="width: 100%"
      >
        <!-- 展开列,点击展开后显示问题和回答 -->
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
                <span>时间：{{ formatDateTime((row as any).created_at) }}</span>

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
        
        <el-table-column label="来源" min-width="160" align="center" >
          <template #default="{ row }">
            {{ (row as any).sources || '无' }}
          </template>
        </el-table-column>
      </el-table>

      <div class="table-footer">
        <span>共 {{ store.records.length }} 条</span>
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="store.records.length"
          layout="prev, pager, next"
          background
        /><!--点击下一页,el-pagination 自动更新 page.value-->
      </div>
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
  padding: 10px 25px;
  margin-bottom: 20px;
}

.page-header h1 {
  font-family: "Arial Black", "Impact", sans-serif;
  font-size: 28px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 6px;
  
}

.page-header p {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-muted);
  
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

.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-top: 4px solid #000000;
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
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
  align-items: center;
  justify-content: flex-start;
}

.expand-question {
  background: var(--brand-gold);
  border: 2px solid #000;
  border-bottom: none;
}

.expand-answer {
  background: var(--bg-sidebar);
  border: 2px solid #000;
  border-left: 3px solid var(--brand-coral);
  border-top: none;
  border-bottom: none;
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
