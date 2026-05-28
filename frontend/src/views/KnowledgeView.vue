<script setup lang="ts">// 知识库视图test
import { useDocumentStore } from '../stores/documents'
import { ref, computed, onMounted } from 'vue'
import type { DocumentItem } from '../api/documents'
import { ElMessageBox } from 'element-plus'
import { fileBadge } from '../utils/format'

const store = useDocumentStore()
const search = ref('')
const page = ref(1)
const pageSize = 10
const renameVisible = ref(false)
const renameName = ref('')
const currentDoc = ref<DocumentItem | null>(null)

  // 过滤文档,根据搜索关键词和分页参数
const filteredDocs = computed(() => {
  if (!search.value) return store.documents
  const kw = search.value.toLowerCase()
  // filter过滤文档,根据d是否包含(include)kw筛选文档并返回新的数组
  return store.documents.filter((d) => d.original_name.toLowerCase().includes(kw))
})

// 切分文档列表,10条/页
const pageDocs = computed(() => {
  const start = (page.value - 1) * pageSize// 计算当前页的起始索引
  // slice方法从 新的 filteredDocs.value 中提取当前页的文档,返回新的数组
  return filteredDocs.value.slice(start, start + pageSize)
})

// 打开重命名弹窗
function openRename(doc: DocumentItem) {
  currentDoc.value = doc
  renameName.value = doc.original_name
  renameVisible.value = true
}

async function confirmRename() {
  if (!currentDoc.value || !renameName.value.trim()) return
  await store.doRename(currentDoc.value.file_id, renameName.value.trim())
  renameVisible.value = false
}

// 确认删除文档
function confirmDelete(doc: DocumentItem) {
  ElMessageBox.confirm(
    `确定删除 "${doc.original_name}" 吗？`,
    '删除确认',
    { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
  ).then(() => store.doDelete(doc.file_id))
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

onMounted(() => store.loadDocuments())
</script>

<template>
  <div class="knowledge-page">
    <header class="page-header">
      <div class="header-text">
        <h1>知识库</h1>
        <p>查看和管理所有文档</p>
      </div>
      <div class="search-bar">
        <el-input v-model="search" placeholder="搜索文档..." size="large" clearable />
      </div>
    </header>

    <div class="table-card">
      <el-table :data="pageDocs" v-loading="store.loading" stripe style="width: 100%" size="large">
        <el-table-column prop="file_type" label="类型" width="150">
          <template #default="{ row }">
            <span :class="['badge', row.file_type.toLowerCase()]" style="margin-left:15px">
              {{ fileBadge(row.file_type) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="original_name" label="文件名" min-width="300" show-overflow-tooltip />

        <el-table-column label="上传时间" width="200">
          <template #default="{ row }">
            <span class="date-cell">{{ formatDate(row.created_at) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <button class="op-btn rename-btn" @click="openRename(row)">重命名</button>
            <button class="op-btn delete-btn" @click="confirmDelete(row)">删除</button>
          </template>
        </el-table-column>
      </el-table>

      <div class="table-footer">
        <span>共 {{ filteredDocs.length }} 条</span>
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="filteredDocs.length"
          layout="prev, pager, next"
          background
        />
      </div>
      <!-- 重命名弹窗,(弹窗组件:el-dialog) -->
      <el-dialog v-model="renameVisible" title="重命名文档" width="420px">
        <el-input v-model="renameName" size="large" placeholder="输入新文件名" />
        <template #footer>
          <el-button @click="renameVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRename">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<style scoped>
.knowledge-page {
  padding: 24px 32px;
  width: 100%;
	height: 100%;
	background-color: var(--brand-blue);
}
/* 网格纹理 */
.knowledge-page::before {
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
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background-color: #F0C050;
  border: 3px solid #000000;
  box-shadow: 5px 5px 0px #000000;
  padding: 8px 25px;
}

.header-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-right: 30px;
}

.header-text h1 {
  font-family: "Arial Black", "Impact", sans-serif;
  font-size: 35px;
  font-weight: 900;
  letter-spacing: 10px;
  margin: 0;
}

.header-text p {
  font-family: var(--font-mono);
  font-size: 15px;
  letter-spacing: 2px;
  color: var(--text-muted);
  margin: 0;
}

.search-bar {
  width: 250px;
  border: 1px solid #000000;
  box-shadow: 6px 6px 0px var(--brand-gold);
  margin-left: 30px;
}

.table-card {
  margin-top: 20px;
  border: 3px solid #000000;
  box-shadow: 5px 5px 0px #000000;
  background: #FFFFFF;
}

:deep(.el-table__body td) {
  overflow: visible;
  padding: 10px 0;
}

:deep(.el-table__body td .cell) {
  overflow: visible;
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

.badge {
  display: inline-block;
  padding: 2px 10px;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 800;
  border: 2px solid #000000;
  box-shadow: 2px 2px 0px #000000;
}

.badge.pdf { background: #E85D4A; color: #FFFFFF; }
.badge.docx { background: #2C5F8A; color: #FFFFFF; }
.badge.md { background: #F0C050; color: #000000; }
.badge.txt { background: #E8E3D9; color: #000000; }

.date-cell {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.op-btn {
  display: inline-block;
  padding: 4px 14px;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 800;
  border: 2px solid #000000;
  box-shadow: 2px 2px 0px #000000;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.1s;
  margin-right: 6px;
}
.op-btn:active {
  transform: translate(3px, 3px);
  box-shadow: none;
}
.rename-btn {
  background: #2C5F8A;
  color: #FFFFFF;
}
.rename-btn:hover {
  background: #3A7AB5;
  transform: translate(2px, 2px);
  box-shadow: none;
}
.delete-btn {
  background: #E85D4A;
  color: #FFFFFF;
}
.delete-btn:hover {
  background: #F07060;
  transform: translate(2px, 2px);
  box-shadow: none;
}
</style>
