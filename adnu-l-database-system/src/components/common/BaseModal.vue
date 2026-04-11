<script setup>
defineProps({
  show: Boolean,
  width: { type: String, default: '450px' }
});
defineEmits(['close']);
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" :style="{ width: width }">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 31, 92, 0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: var(--white);
  padding: 30px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}
</style>