import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import './style.css'
import { Clock, Loading, CircleCheck } from '@element-plus/icons-vue'


const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.component('Clock', Clock)
app.component('Loading', Loading)
app.component('CircleCheck', CircleCheck)

app.mount('#app')
