<script setup>
import SideBar from './components/layout/SideBar.vue';
import router from './router';
import { ref } from 'vue';

const isSidebarCollapsed = ref(false);

const handleSidebarCollapse = (collapsed) => {
  isSidebarCollapsed.value = collapsed;
};
</script>

<template>
  <div class="app-layout">
    <SideBar @collapse-change="handleSidebarCollapse" />

    <main :class="['main-body', { 'sidebar-collapsed': isSidebarCollapsed }]">
      <router-view />
    </main>
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
</style>