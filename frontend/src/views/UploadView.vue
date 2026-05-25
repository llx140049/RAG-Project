<script setup lang="ts">
	import { reactive } from 'vue'
	import { useDocumentStore } from '../stores/documents'
	import { ElMessage } from 'element-plus'
	import type { UploadFile } from 'element-plus'
	import { fileBadge, formatSize } from '../utils/format'
	import { CircleCheck, Clock, Upload, WarningFilled } from '@element-plus/icons-vue'

	interface QueueItem {
		uid:number
		name:string
		size:number
		type:string
		file:File
		status: 'waiting' | 'uploading' | 'error' | 'done'
	}

	const queue = reactive<QueueItem[]>([])// 上传队列,存储待上传的文件
		const store = useDocumentStore()
	let uidCounter=0

	//文件一旦被选择或拖入，(@change:onFileChange)就触发该函数:验证文件格式,并添加到上传队列
	function onFileChange(uploadFile: UploadFile) {
		const rawFile = uploadFile.raw!//获取原始文件对象
		const ext = rawFile.name.split('.').pop()?.toLowerCase()//获取文件扩展名,并转换为小写
		if (!ext || !['pdf', 'docx', 'txt', 'md'].includes(ext)) {
			ElMessage.error('请上传PDF、DOCX、TXT或MD格式的文档')
			return
		}
    // 验证通过后,将文件添加到上传队列,并设置状态为 waiting
    // 等待上传组件触发上传事件
		queue.push({
			uid: ++uidCounter,
			name: rawFile.name,
			size: rawFile.size ?? 0,
			type: ext,
			file: rawFile,
			status: 'waiting',
		})
    // 触发上传队列处理函数,开始处理上传任务(统一处理,易扩展)
		processQueue()
	}

	async function processQueue(){
		for(const item of queue){
			if(item.status!=='waiting') continue
      // 只处理等待状态的文件,其他状态的文件直接跳过
      // 等待上传组件触发上传事件,并设置状态为 uploading
			item.status='uploading'
			try {
				await store.doUpload(item.file)
				item.status='done'
			} catch (error) {
				item.status='error'
				ElMessage.error('上传失败')
			}
		}
	}

</script>







<template>
  <div class="upload-page">
		<header class="page-header">
			<h1>上传文档</h1>
			<p>充实你的知识库</p>
		</header>

		<div class="upload-layout">
			<!--左侧上传区-->
			<div class="dropzone">
        <!--el-upload 内部会包一层可点击区域，点击这个区域里的内容时，会转发到隐藏的 <input type="file">,然后触发change事件-->
        <!--accept使系统文件面板里帮用户过滤可选文件,只显示PDF、DOCX、TXT、MD格式的文件-->
				<el-upload
					class="dropzone-upload"
					drag
					multiple
					@change="onFileChange"
					:auto-upload="false"
					:show-file-list="false"
					accept=".pdf,.docx,.txt,.md"
				>
					<div class="dropzone-content">
						
						<i class="iconfont icon-shangchuan" style="font-size: 80px;color: var(--text-muted);"></i>
						<span class="drop-text">拖拽文件到此处或点击选择</span>
            <!--点击事件冒泡到上传组件后，被上传组件接管,按钮没有实际功能-->
						<button class="pick-btn">选择文件</button>
					</div>
				</el-upload>
			</div>
			<!--右侧上传队列-->
			<div class="upload-list">

				<h2>上传列表</h2>
				<div class="list-scroll">
					<div v-if="queue.length===0" class="empty-hint">暂无上传任务</div>
			
					<div v-for="item in queue" :key="item.uid" class="queue-card">
						<span :class="['type-badge',item.type]">{{fileBadge(item.type)}}</span>
						<div class="list-info">
							<span class="list-name">{{item.name}}</span>
							<span class="list-size">{{formatSize(item.size)}}</span>
						</div>
						<span class="status-icon">
							<Clock v-if="item.status==='waiting'" style="width:22px;height:22px" />
							<Upload v-if="item.status==='uploading'" style="width:22px;height:22px" />
							<CircleCheck v-if="item.status==='done'" style="width:22px;height:22px;color:#0F8F67" />
							<WarningFilled v-if="item.status==='error'" style="width:22px;height:22px;color:#E85D4A" />
						</span>
					</div>

				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.upload-page {
  padding: 40px;
  width: 100%;
	height: 100%;
	background-color: var(--brand-blue);
}
/* 网格纹理 */
.upload-page::before {
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
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width:40%;
	background-color: #F0C050;
	border: 3px solid #000000;
	box-shadow: var(--box-shadow);
	padding: 8px 25px;
	margin-bottom: 28px;
}

.page-header h1 {
  font-family: "Arial Black", "Impact", sans-serif;
  font-size: 28px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 0 0 6px 0;
}

.page-header p {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-muted);
  margin: 0;
}

.upload-layout {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 24px;
}

.dropzone {
  border: 4px solid #000000;
  box-shadow: var(--box-shadow);
  background: #FFFFFF;
  height: 400px;
  display: flex;/*开启flex布局,flex很适合做这种“让一层套一层都撑满父容器”的事情*/
  align-items: stretch;
  justify-content: stretch;
  overflow: hidden;
  position: relative;
}

.dropzone-upload {
  flex: 1;/*占满父元素*/
  width: 100%;
  height: 100%;
  display: block;
}

.dropzone :deep(.el-upload) {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: stretch;
  align-items: stretch;
}

.dropzone :deep(.el-upload.is-drag) {
  display: flex;
  flex: 1;
  width: 100%;
  height: 100%;
}

.dropzone :deep(.el-upload-dragger) {
  flex: 1;
  width: 100%;
  height: 100%;
  border: none;
  background: transparent;
  display: block;
  box-sizing: border-box;
  padding: 0;/*覆盖默认值*/
  margin: 0;/*too*/
  border-radius: 0;
}

.dropzone :deep(.el-upload-dragger.is-dragover) {
  padding: 0;/*too*/
  border: none;
  background: #f0c0505e;
}

.dropzone :deep(.el-upload-dragger.is-dragover) .dropzone-content {
  transform: scale(1.04);
}

.dropzone-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  width: 100%;
  min-width: 100%;
  height: 100%;
  min-height: 100%;
  align-self: stretch;
  padding: 20px;
  box-sizing: border-box;
  text-align: center;
  transition: transform 0.1s, box-shadow 0.1s;
}


.drop-text {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-muted);
}

.pick-btn {
  padding: 10px 24px;
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
  background: var(--brand-coral);
  color: #FFFFFF;
  border: 3px solid #000000;
  box-shadow: 4px 4px 0px #000000;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.1s;
}
.pick-btn:hover {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0px #000;
}
.pick-btn:active {
  transform: translate(3px, 3px);
  box-shadow: none;
}

.upload-list {
  background: #FFFFFF;
  border: 4px solid #000000;
  box-shadow: 6px 6px 0px #000000;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.upload-list h2 {
  font-family: "Arial Black", "Impact", sans-serif;
  font-size: 18px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 8px 0;
  padding-bottom: 12px;
  border-bottom: 4px solid #000000;
}

.empty-hint {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-muted);
  text-align: center;
  padding: 40px 0;
}
.list-scroll {
  max-height: 480px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-right: 4px;
}

.queue-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 3px solid #000000;
  box-shadow: 3px 3px 0px #000000;
  background: #FAFAFA;
}

.type-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 900;
  border: 3px solid #000000;
  box-shadow: 2px 2px 0px #000000;
  flex-shrink: 0;
}

.type-badge.pdf  { background: #E85D4A; color: #FFFFFF; }
.type-badge.docx { background: #2C5F8A; color: #FFFFFF; }
.type-badge.md   { background: #F0C050; color: #000000; }
.type-badge.txt  { background: #E8E3D9; color: #000000; }

.list-info {
  flex: 1;
  min-width: 0;
}

.list-name {
  display: block;
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 800;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.list-size {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
}

.status-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;

}
</style>
