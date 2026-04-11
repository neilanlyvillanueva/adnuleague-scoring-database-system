<script setup>
import { reactive, watch } from 'vue';

const props = defineProps({
  show: Boolean,
  team: Object
});

const emit = defineEmits(['close', 'save']);

const form = reactive({
  name: '',
  color: '#0038A8'
});

watch(() => props.team, (newTeam) => {
  if (newTeam) {
    form.name = newTeam.name;
    form.color = newTeam.color;
  } else {
    form.name = '';
    form.color = '#0038A8';
  }
}, { immediate: true });

const handleSave = () => {
  if (!form.name.trim()) {
    alert('Please enter a team name');
    return;
  }
  emit('save', { ...form });
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content team-modal">
      <div class="modal-header-section">
        <h3>{{ team ? 'Edit Team' : 'Register New Team' }}</h3>
        <p class="modal-subtitle">Configure team identity and branding.</p>
      </div>

      <div class="modal-form-body">
        <div class="form-group">
          <label>Team / College Name</label>
          <input v-model="form.name" type="text" class="modal-input" placeholder="e.g. Engineering">
        </div>

        <div class="form-group">
          <label>Representative Color</label>
          <div class="color-picker-row">
            <input v-model="form.color" type="color" class="color-circle-input">
            <span class="color-code">{{ form.color.toUpperCase() }}</span>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn-ghost" @click="emit('close')">Cancel</button>
        <button class="btn-primary" @click="handleSave">Save changes</button>
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
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  max-width: 450px;
  width: 100%;
  border-top: 6px solid var(--adnu-gold);
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

.modal-form-body {
  padding: 0 24px 24px 24px;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  font-weight: 700;
  font-size: 0.75rem;
  color: var(--adnu-blue-navy);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-family: var(--font-main);
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.modal-input:focus {
  outline: none;
  border-color: var(--adnu-blue-dark);
}

/* Color Picker UI */
.color-picker-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
}

.color-circle-input {
  border: none;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  cursor: pointer;
  background: none;
  padding: 0;
}

.color-circle-input::-webkit-color-swatch {
  border-radius: 50%;
  border: 2px solid var(--border-color);
}

.color-code {
  font-family: monospace;
  font-weight: 700;
  background: var(--white);
  padding: 8px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
