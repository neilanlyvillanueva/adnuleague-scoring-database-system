<script setup>
import SideBar from './components/layout/SideBar.vue';
import router from './router';
</script>

<template>
  <div class="app-layout">
    <SideBar />

    <main class="main-body">
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
  /* Match the SideBar.vue width exactly */
  margin-left: 260px; 
  background-color: var(--bg-gray-light);
  min-height: 100vh;
  /* Added padding so dashboard content doesn't hit the screen edges */
  padding: 40px; 
  box-sizing: border-box;
}
</style>