import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchDocuments, renameDocument, deleteDocument, uploadDocument, type DocumentItem } from '../api/documents'
import { ElMessage } from 'element-plus'// 引入 Element Plus 的消息提示组件

// 文档状态管理
// 定义一个名为 documents 的状态管理模块
// 它包含文档列表、文档总数、加载状态等状态
// 以及加载文档、重命名文档、删除文档、上传文档等操作
export const useDocumentStore = defineStore('documents',()=>{
        const documents = ref<DocumentItem[]>([])// 文档列表数组
        const total=ref(0)// 文档总数
        const loading=ref(false)// 加载状态,控制 loading 动画

        // 加载文档,返回 Promise,等待加载完成
        // 加载成功后,更新文档列表和总数
        async function loadDocuments(skip=0,limit=20){
            loading.value=true
            try{
                // fetchDocuments 函数返回一个 Promise，等待它解析为一个 DocumentItem 数组
                const res=await fetchDocuments(skip,limit)
                documents.value=res.data
                total.value=res.data.length
            }catch(err){
                ElMessage.error('加载文档失败')// 显示错误消息
            }finally{
                loading.value=false
            }
        }

        async function doRename (fileId:string,newName:string){
            await renameDocument(fileId,newName)
            await loadDocuments()
            ElMessage.success('重命名成功')
        }

        async function doDelete (fileId:string){
            await deleteDocument(fileId)
            // 删除成功后，刷新文档列表
            documents.value=documents.value.filter((doc)=>doc.file_id!==fileId)
            ElMessage.success('删除成功')
        }

        // 上传文档,返回 Promise,等待上传完成
        // 上传成功后,刷新文档列表和总数
        async function doUpload (file:File){
            loading.value=true
            try{
                await uploadDocument(file)
                await loadDocuments()
                ElMessage.success('上传成功')
            }catch(err){
                ElMessage.error('上传失败')
            }finally{
                loading.value=false
            }
        }

        return {
            documents,
            total,
            loading,
            loadDocuments,
            doRename,
            doDelete,
            doUpload,
        }
})
