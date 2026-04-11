<script setup>
import SideBar from './components/layout/SideBar.vue';
import router from './router';
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isSidebarCollapsed = ref(false);

const handleSidebarCollapse = (collapsed) => {
  isSidebarCollapsed.value = collapsed;
};

// Check if current route is login page (hide sidebar)
const isLoginPage = computed(() => route.path === '/login');
</script>

<template>
  <div class="app-layout">
    <SideBar v-if="!isLoginPage" @collapse-change="handleSidebarCollapse" />

    <main
      v-if="!isLoginPage"
      :class="['main-body', { 'sidebar-collapsed': isSidebarCollapsed }]"
    >
      <router-view />
    </main>
    <router-view v-else />
  </div>
</template>

<style>
.app-layout {
  display: flex;
  width: 100%;
  min-height: 100vh;
}

.main-body {
  flex-grow: 1;
  margin-left: 260px;
  background-color: var(--bg-gray-light);
  min-height: 100vh;
  padding: 40px;
  box-sizing: border-box;
  transition: margin-left 0.3s ease;
}

/* Collapsed sidebar state */
.main-body.sidebar-collapsed {
  margin-left: 70px;
}

/* Login page - full screen, no sidebar */
body:has(.login-page) {
  margin: 0;
  padding: 0;
}
</style>