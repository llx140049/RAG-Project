<script setup lang="ts">
	import {ref,nextTick,watch} from 'vue'
	import {askQuestion} from '../api/qa'
	import {ElMessage} from 'element-plus'

	interface Message {
		role:'user'|'assistant'
		content:string
		time:string
		sources?: string
	}

	const messages = ref<Message[]>([])
	const inputText = ref('')// 输入框内容
	const loading = ref(false)
	const listRef = ref<HTMLElement>()
	const STORAGE_KEY='qa-chat-archive'

	// 格式化时间
	function formatTime(){
		const now=new Date()
		return now.toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit',second:'2-digit'})
	}

	async function sendMessage(){
		const text=inputText.value.trim()// 去掉首尾空格
		if(!text||loading.value) return// 空消息或正在加载,直接返回
		// 添加用户消息到列表
		messages.value.push({role:'user',content:text,time:formatTime()})
		inputText.value=''
		loading.value=true
		await scrollToBottom()// 滚动到最底部

		try {
			const res=await askQuestion(text)
			// 处理响应,添加到消息列表,
			messages.value.push({
				role:'assistant',
				content:res.data.answer,
				time:formatTime(),
				sources:res.data.sources,
			})
		}catch (error: any) {
			const msg = error?.response?.data?.detail || error?.message || '回答失败，请稍后重试'
			ElMessage.error(`回答失败：${msg}`)
		}finally {
			loading.value=false
			await scrollToBottom()// 滚动到最底部
		}

	}

	// 滚动到最底部
	async function scrollToBottom(){
		await nextTick()// 等待 DOM 更新完成
		if(listRef.value){
			listRef.value.scrollTop=listRef.value.scrollHeight//
		}
	}

	function clearMessages(){
		messages.value=[]
		localStorage.removeItem(STORAGE_KEY)// 清除本地存储中的对话记录
	}

	function saveChat(){
		if(messages.value.length===0){
			ElMessage.warning('请先提问')
			return
		}
		localStorage.setItem(STORAGE_KEY,JSON.stringify(messages.value))// 保存对话记录
		ElMessage.success('对话已保存')
	}

	const saved=localStorage.getItem(STORAGE_KEY)// 从本地存储中获取对话记录
	if(saved){
		try{
			messages.value=JSON.parse(saved)// 解析对话记录
		}catch (error) {
			ElMessage.error('对话记录格式错误')
		}
	}


	function onKeydown(e:KeyboardEvent){
		if(e.key==='Enter'&&!loading.value){
			e.preventDefault()
			// 阻止默认换行行为
			sendMessage()
		}
	}

	// 监听消息列表变化,滚动到最底部
	watch(messages,() => scrollToBottom(),{deep:true})


</script>

<template>
	<div class="qa-page">
		<header class="qa-header">
			<div class="header-text">
				<h1>智能问答</h1>
				<p>基于上传文档的知识库问答，每次对话为独立会话</p>
			</div>
			<div class="header-actions">
				<button class="clear-btn" @click="saveChat">保存对话</button>
				<button class="clear-btn" @click="clearMessages">清除对话</button>
			</div>
		</header>

		<div class="qa-body">
			<div ref="listRef" class="message-list">
				<div v-if="messages.length===0" class="empty-hint">开始提问吧!</div>
				<div
					v-for="(msg,i) in messages"
					:key="i"
					:class="['message',msg.role==='user'?'user-msg':'ai-msg']"
				>
					<span class="msg-role">{{ msg.role==='user'?'用户':'助手' }}</span>
					<p class="msg-content">{{ msg.content }}</p>
					<p v-if="msg.role==='assistant' && msg.sources && msg.sources !== '无'" class="msg-sources">
						来源：{{ msg.sources }}
					</p>
					<time class="msg-time">{{ msg.time }}</time>
				</div>

				<div v-if="loading" class="message ai-msg loading-msg">
					<span class="msg-role">助手</span>
					<p class="msg-content">思考中...</p>
				</div>
			</div>

			<div class="input-row">
        <!-- 输入框 ,问题放进inputText--> 
				<el-input
					v-model="inputText"
					type="textarea"
					:rows="1"
					placeholder="输入你的问题..."
					:disabled="loading"
					resize="none"
					@keydown="onKeydown"
				/>
				<button class="send-btn" :disabled="loading||!inputText.trim()" @click="sendMessage">发送</button>

			</div>
		</div>
	</div>
</template>

<style scoped>
.qa-page {
  display: flex;
  flex-direction: column;
  width: 100%;
	height: 100%;
  background: var(--brand-blue);
}
/* 网格纹理 */
.qa-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255, 255, 255, 0.123) 39px, rgba(255,255,255,0.123) 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,255,255,0.123) 39px, rgba(255,255,255,0.123) 40px);
  pointer-events: none;
  z-index: 0;
}

.qa-header {
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #F0C050;
  border: 3px solid #000000;
  box-shadow: 5px 5px 0px #000000;
  padding: 12px 28px;
  margin: 24px 32px 0;
}

.header-text h1 {
  font-family: "Arial Black", "Impact", sans-serif;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: 6px;
  margin: 0;
  text-transform: uppercase;
}

.header-text p {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  margin: 4px 0 0;
}

.header-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
.clear-btn {
  padding: 10px 20px;
  font-family: var(--font-mono);
  font-size: 15px;
  font-weight: 900;
	color: #FFFFFF;
  text-transform: uppercase;
  background: var(--brand-blue);
  border: 2px solid #000000;
  box-shadow: 3px 3px 0px #000000;
  cursor: pointer;
}

.clear-btn:hover {
  transform: translate(2px, 2px);
  box-shadow: 1px 1px 0px #000;
}
.clear-btn:active {
  transform: translate(3px, 3px);
  box-shadow: none;
}
.qa-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 20px 32px 24px;
  overflow: hidden;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #FFFFFF;
  border: 4px solid #000000;
  box-shadow: 6px 6px 0px #000000;
}

.empty-hint {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-muted);
  text-align: center;
  padding: 60px 0;
}
.message {
  position: relative;
  padding: 12px 20px;
  border: 3px solid #000000;
  box-shadow: 3px 3px 0px #000000;
  max-width: 80%;
}

.user-msg {
  align-self: flex-end;
  background: #F0C050;
}

.ai-msg {
  align-self: flex-start;
  background: #FFFFFF;
  border-left: 5px solid var(--brand-coral);
}

.msg-role {
  display: block;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #000000;
  margin-bottom: 5px;
}

.msg-content {
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
  color: var(--text-primary);
  margin: 0;
  white-space: pre-wrap;/* 保留换行符 */
}

.msg-time {
  display: block;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  margin-top: 10px;
  text-align: right;
}

.msg-sources {
  margin: 10px 0 0;
  padding: 8px 10px;
  border: 2px solid #000000;
  background: #F7F7F7;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  line-height: 1.5;
  color: var(--text-muted);
  white-space: pre-wrap;
}

.loading-msg .msg-content {
  color: var(--text-muted);
  font-style: italic;
}
.input-row {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 15px;/* 输入框与发送按钮之间的间距 */
  padding: 8px;
  background: var(--brand-blue);
  border: 4px solid #000000;
  margin-top: 20px;
}

.send-btn {
  flex-shrink: 0;
  padding: 0 28px;
  font-family: var(--font-mono);
  font-size: 15px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 2px;
  background: var(--brand-coral);
  color: #FFFFFF;
  border: 2px solid #000000;
  box-shadow: 3px 3px 0px #000000;
  cursor: pointer;
}

.send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 发送按钮点击效果 */
.send-btn:not(:disabled):hover {
  transform: translate(2px, 2px);
  box-shadow: 1px 1px 0px #000;
}
.send-btn:not(:disabled):active {
  transform: translate(3px, 3px);
  box-shadow: none;
}
/* 输入框样式 */
.input-row :deep(.el-textarea__inner) {
  border: 1px solid #000000 !important;
  border-radius: 0 !important;
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 700;
  resize: none;
  padding: 6px 12px;
}
/* 输入框聚焦效果 */
.input-row :deep(.el-textarea__inner:focus) {
  box-shadow: 3px 3px 0px var(--brand-coral) !important;
  border-color: var(--brand-coral) !important;
}
/* 输入框禁用效果 */
.input-row :deep(.el-textarea__inner:disabled) {
  background: #F5F5F5;
  opacity: 0.6;
}
</style>
