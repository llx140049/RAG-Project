import { defineConfig } from 'vite'//Vite 提供的配置辅助函数，为 TypeScript 提供智能提示和类型检查
import vue from '@vitejs/plugin-vue'//Vite 的 Vue 插件，让 Vite 能识别和编译 .vue 单文件组件

//
export default defineConfig({
  plugins: [vue()],//注册 Vue 插件,让 Vite 能识别和编译 .vue 单文件组件
  server: {
    proxy: {
      '/api': {//匹配规则：当前端请求路径以 /api 开头时触发代理
        target: 'http://127.0.0.1:8000',//转发的目标地址
        changeOrigin: true,//修改请求头的 Origin 为目标地址，避免后端校验拒绝
        rewrite: (path)=> path.replace(/^\/api/, ''),//将请求路径中的 /api 前缀去掉,发送给后端
      },
    },
  },
})
