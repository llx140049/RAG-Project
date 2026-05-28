import { defineStore } from 'pinia'
import {ref} from 'vue'
import {getHistoryList,getHistoryDetail,deleteHistory,type HistoryItem} from '../api/history'

export const useHistoryStore=defineStore('history',()=>{
    const records=ref<HistoryItem[]>([])
    const loading=ref(false)//是否正在加载中
    const total=ref(0)//总记录数

    // 加载历史记录
    // skip: 跳过记录数
    // limit: 每页记录数
    async function loadHistory(skip=0, limit=10) {
        loading.value=true
        try {
            const res=await getHistoryList(skip, limit)//获取历史记录列表
            records.value=res.data
            total.value=records.value.length
        } catch (error) {
            console.error('加载历史记录失败:', error)
        } finally {
            loading.value=false
        }
    }

    async function loadDetail(id:number):Promise<HistoryItem|null> {
        try {
            const res=await getHistoryDetail(id)
            return res.data
        } catch (error) {
            console.error('加载历史记录详情失败:', error)
            return null
        }
    }

    async function clearHistory() {
        await deleteHistory()
        records.value = []
        total.value = 0
    }

    return {records,loading,total,loadHistory,loadDetail,clearHistory}
})