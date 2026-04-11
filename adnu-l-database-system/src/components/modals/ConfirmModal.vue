<script setup>
defineProps({
  show: Boolean,
  title: String,
  message: String,
  confirmText: { type: String, default: 'Confirm' },
  cancelText: { type: String, default: 'Cancel' },
  type: { type: String, default: 'danger' } // danger, warning, info
});

defineEmits(['close', 'confirm']);
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div :class="['modal-content', 'confirm-modal', type]">
      <div class="modal-icon">
        <i :class="type === 'danger' ? 'fas fa-exclamation-triangle' : type === 'warning' ? 'fas fa-exclamation-circle' : 'fas fa-info-circle'"></i>
      </div>
      <h3>{{ title }}</h3>
      <p>{{ message }}</p>
      <div class="modal-actions">
        <button class="btn-ghost" @click="$emit('close')">{{ cancelText }}</button>
        <button :class="['btn-primary', type]" @click="$emit('confirm')">{{ confirmText }}</button>
      </div>
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
  padding: 30px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.modal-content.danger { border-top: 6px solid var(--adnu-danger); }
.modal-content.warning { border-top: 6px solid var(--adnu-gold); }
.modal-content.info { border-top: 6px solid var(--adnu-blue-dark); }

.modal-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.danger .modal-icon { color: var(--adnu-danger); }
.warning .modal-icon { color: var(--adnu-gold); }
.info .modal-icon { color: var(--adnu-blue-dark); }

.modal-content h3 {
  margin: 0 0 10px 0;
  font-size: 1.3rem;
  color: var(--adnu-blue-navy);
}

.modal-content p {
  margin: 0 0 25px 0;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-primary.danger {
  background: var(--adnu-danger);
}

.btn-primary.danger:hover {
  background: var(--adnu-danger-strong);
}
</style>
