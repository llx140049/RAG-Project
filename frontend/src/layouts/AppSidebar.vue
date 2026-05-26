
<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

onMounted(() => {
  if (auth.token && !auth.user) {
    auth.fetchUser()
  }
})
</script>
<template>
    <div class="app-shell">
        <!--布局组件里，整体结构是 aside + main-->
        <aside class="sidebar">
            <!-- 品牌区域 -->
            <div class="brand">
                <img src="/assets/logo.svg?v=2" alt="logo" class="logo"/>
                <div>
                    <strong class="brand-name">LCRAG</strong>
                </div>
            </div>
            <!-- 导航区域,点击仅改变 URL 路径，侧边栏自身不刷新 -->
            <nav class="nav-list">
                <router-link to="/knowledge" class="nav-item">
                    <i class="iconfont icon-tiku"></i> 知识库
                </router-link>
                <router-link to="/upload" class="nav-item">
                    <i class="iconfont icon-shangchuan"></i> 上传文档
                </router-link>
                <router-link to="/qa" class="nav-item">
                    <i class="iconfont icon-tubiaozhuanqu-09"></i> 智能问答
                </router-link>
                <router-link to="/history" class="nav-item">
                    <i class="iconfont icon-lishijilu"></i> 历史记录
                </router-link>
                <router-link to="/settings" class="nav-item">
                    <i class="iconfont icon-shezhi"></i> 设置
                </router-link>
            

                <div class="profile">
                    <span class="head-picture">{{ auth.user?.username?.charAt(0) || 'A' }}</span>
                    <div class="profile-info">
                        <strong class="username">{{ auth.user?.username  }}</strong>
                        <span class="profile-word">{{ auth.signature }}</span>
                    </div>
                </div>
            </nav>
        </aside>

        <!-- 主内容区域 -->
        <main class="main">
            <!--router-view 就是一个路由组件显示窗口，当前地址匹配到哪个页面组件，就把哪个页面渲染到这个位置-->
            <router-view/>
        </main>
    </div>
</template>

<style scoped>
    .app-shell {
        display: flex;
        height: 100vh;
        overflow: hidden;
    }
    .sidebar {
        display: flex;
        flex-direction: column;
        width: 230px;
        background: var(--bg-sidebar);
        border-right: 3px solid var(--border-warm);
    }
    .main {
        flex: 1;
        background: var(--bg-cream);
        overflow-y: auto;
        overflow-x: hidden;
    }
    .brand {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding-bottom: 15px;
        margin-bottom: -15px;
    }
    .logo {
        margin-left: -30px;
        width: 120px;
        height: 120px;
        z-index: 1;
    }
    .brand-name {
        display: block;
        margin-left: -24px;
        font-size: 25px;
        font-weight: 700;
        letter-spacing: 2px;
        color: var(--text-primary);
    }
    .nav-list {
        display: flex;
        flex-direction: column;
        gap: 25px;
        padding: 0 16px;
    }
    .nav-item {
        display: block;
        padding: 14px 16px;
        text-align: left;
        font-size: 17px;
        font-weight: 1000;
        color: var(--border-warm);
        background: var(--bg-sidebar);
        border-radius: 0;
        border: 2px solid var(--border-warm);
        box-shadow: var(--box-shadow-small);
        text-decoration: none;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    .nav-item:hover {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #000;
        background: var(--brand-coral);
        color: var(--text-primary);
    }
    .nav-item:active {
        transform: translate(3px, 3px);
        box-shadow: none;
    }
    .nav-item.router-link-active {
        background: var(--brand-gold);
        color: var(--text-primary);
    }
    .profile {
        display: flex;
        width: 200px;
        background: var(--brand-blue);
        gap: 10px;
        padding: 8px 12px;
        margin-top: 210px;
        border: 2px solid #000;
        box-shadow: var(--box-shadow-small);
    }
    .head-picture {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 2px;
        width: 40px;
        height: 40px;
        border: 3px solid var(--border-warm);
        border-radius: 50%;
        background: var(--brand-gold);
        color: var(--text-primary);
        font-size: 14px;
        font-weight: 900;
        z-index: 1;
    }
    .profile-info {
        flex: 1;/* 占满剩余空间 */
        min-width: 0;
    }
    .username {
        display: block;
        margin-top: 2px;
        font-size: 18px;
        font-weight: 900;
        color: var(--brand-gold);
        /* 单行,超出部分省略号 */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .profile-word {
        display: block;
        font-size: 12px;
        font-weight: 700;
        color: #FFFFFF;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;


    }

    .nav-item i {
        margin-right: 4px;
        font-size: 24px;
        font-weight: 1000;
        color: var(--brand-blue);
        vertical-align: middle;
    }
    
    .logout-btn {
        display: block;
        width: calc(100% - 32px);
        margin: 8px 16px 16px 16px;
        padding: 10px 16px;
        font-size: 15px;
        font-weight: 800;
        color: var(--text-primary);
        background: var(--brand-coral);
        border: 2px solid var(--border-warm);
        box-shadow: 3px 3px 0px var(--border-warm);
        cursor: pointer;
        text-align: center;
    }
    .logout-btn:hover {
        background: #E85D4A;
        color: #FFFFFF;
    }
</style>
