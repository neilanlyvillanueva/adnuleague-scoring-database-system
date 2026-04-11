<script setup>
import { reactive } from 'vue';

const props = defineProps({
  show: Boolean,
  scoringSystems: Array,
  selectedSystemId: [Number, String]
});

const emit = defineEmits(['close', 'select', 'add-custom']);

const form = reactive({
  name: '',
  description: ''
});

const handleSelect = (systemId) => {
  emit('select', systemId);
};

const handleAddCustom = () => {
  if (!form.name.trim()) {
    alert('Please enter a scoring system name');
    return;
  }
  emit('add-custom', { ...form });
  form.name = '';
  form.description = '';
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content scoring-modal">
      <div class="modal-header-section">
        <h3>Manage Scoring Systems</h3>
        <p class="modal-subtitle">Choose from pre-defined systems or create a custom one.</p>
      </div>

      <div class="scoring-systems-list">
        <h4>Pre-defined Systems</h4>
        <div class="scoring-systems-grid">
          <div
            v-for="system in scoringSystems?.filter(s => s.type === 'predefined')"
            :key="system.id"
            :class="['scoring-system-card', { selected: selectedSystemId === system.id }]"
            @click="handleSelect(system.id)"
          >
            <div class="scoring-system-info">
              <h5>{{ system.name }}</h5>
              <p>{{ system.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="custom-system-section">
        <label class="form-label">Add Custom Scoring System</label>
        <input v-model="form.name" type="text" class="modal-input" placeholder="System name...">
        <input v-model="form.description" type="text" class="modal-input" placeholder="Description..." style="margin-top: 8px;">
      </div>

      <div class="modal-actions">
        <button class="btn-ghost" @click="emit('close')">Close</button>
        <button class="btn-primary" @click="handleAddCustom">Add Custom System</button>
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
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border-top: 6px solid var(--adnu-blue-dark);
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

.scoring-systems-list {
  padding: 0 24px 20px 24px;
}

.scoring-systems-list h4 {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--adnu-blue-navy);
  text-transform: uppercase;
  margin: 0 0 12px 0;
}

.scoring-systems-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.scoring-system-card {
  padding: 15px;
  background: var(--bg-gray-light);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.scoring-system-card:hover {
  border-color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
}

.scoring-system-card.selected {
  border-color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
}

.scoring-system-info h5 {
  margin: 0 0 6px 0;
  font-size: 0.95rem;
  color: var(--adnu-blue-navy);
  font-weight: 600;
}

.scoring-system-info p {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.custom-system-section {
  padding: 0 24px 20px 24px;
  border-top: 1px solid var(--border-color);
}

.form-label {
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

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
