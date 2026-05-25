import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/403',
      name: 'forbidden',
      component: () => import('../views/ForbiddenView.vue'),
      meta: { guest: true },
    },
    {
      //嵌套路由 : 根路径 / 先加载布局组件 AppSidebar.vue
      // 主路由Sidebar,包含子路由:上传,知识库,问答,历史记录,设置
      path: '/',
      component: () => import('../layouts/AppSidebar.vue'),
      meta: { requiresAuth: true },
      redirect: '/knowledge',
      children: [
        {
          path: 'knowledge',
          name: 'knowledge',
          component: () => import('../views/KnowledgeView.vue'),
        },
        {
          path: 'upload',
          name: 'upload',
          component: () => import('../views/UploadView.vue'),
        },
        {
          path: 'qa',
          name: 'qa',
          component: () => import('../views/QAView.vue'),
        },
        {
          path: 'history',
          name: 'history',
          component: () => import('../views/HistoryView.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/SettingsView.vue'),
        },

      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: { guest: true },
    },
  ],
})

// 路由守卫,检查用户是否已登录
// 如果未登录，重定向到登录页
// 如果已登录，继续导航
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
