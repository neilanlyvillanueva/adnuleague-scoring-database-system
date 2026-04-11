<template>
  <header class="dashboard-header">
    <div class="welcome-text">
      <h1>{{ title }}</h1>
      <p v-if="subtitle">{{ subtitle }}</p>
    </div>
    
    <div class="header-actions">
      <slot name="actions"></slot>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: String,
  subtitle: String
});
</script>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: space-between; /* Pushes text left, actions right */
  align-items: flex-end;         /* Aligns button with the bottom of the title */
  margin-bottom: 40px;
  width: 100%;                   /* Ensures it spans the whole page */
}

.welcome-text h1 {
  font-size: 2rem;
  color: var(--adnu-blue-navy);
  margin: 0;
}

.welcome-text p {
  color: var(--text-muted);
  margin: 5px 0 0 0;
  font-size: 1rem;
}

/* Optional: Ensures buttons inside the actions area have a little gap */
.header-actions {
  display: flex;
  gap: 12px;
}
</style>