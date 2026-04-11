<script setup>
defineProps({
  show: Boolean,
  title: String,
  subtitle: String,
  width: { type: String, default: '500px' },
  accentColor: { type: String, default: 'gold' }
});

defineEmits(['close']);
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" :style="{ width, borderTopColor: accentColor }">
      <div v-if="title" class="modal-header-section">
        <h3>{{ title }}</h3>
        <p v-if="subtitle" class="modal-subtitle">{{ subtitle }}</p>
      </div>
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  max-height: 90vh;
  overflow-y: auto;
  border-top-width: 6px;
  border-top-style: solid;
}

.modal-header-section {
  padding: 24px 24px 16px 24px;
}

.modal-header-section h3 {
  margin: 0 0 4px 0;
  font-size: 1.4rem;
  color: var(--adnu-blue-navy);
  font-weight: 700;
}

.modal-subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 0;
}
</style>
