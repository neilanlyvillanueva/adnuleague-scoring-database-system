<script setup>
import { reactive, watch } from 'vue';

const props = defineProps({
  show: Boolean,
  event: Object,
  scoringSystems: Array,
  categories: Array
});

const emit = defineEmits(['close', 'save']);

const categories = ['All', 'Sports', 'Cultural', 'Academic', 'Laro ng Lahi'];

const form = reactive({
  name: '',
  category: 'Sports',
  customCategory: '',
  scoringSystemId: null,
  thresholdIncremental: false,
  sets: null,
  matchupSystem: '1v1'
});

watch(() => props.event, (newEvent) => {
  if (newEvent) {
    form.name = newEvent.name;
    form.category = newEvent.category;
    form.scoringSystemId = newEvent.scoringSystemId;
    form.thresholdIncremental = newEvent.thresholdIncremental;
    form.sets = newEvent.sets;
    form.matchupSystem = newEvent.matchupSystem;
  } else {
    form.name = '';
    form.category = 'Sports';
    form.customCategory = '';
    form.scoringSystemId = null;
    form.thresholdIncremental = false;
    form.sets = null;
    form.matchupSystem = '1v1';
  }
}, { immediate: true });

const handleSave = () => {
  const finalCategory = form.category === 'Custom' ? form.customCategory : form.category;
  emit('save', {
    ...form,
    category: finalCategory,
    sets: form.thresholdIncremental ? form.sets : null
  });
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content event-modal">
      <div class="modal-header-section">
        <h3>{{ event ? 'Edit Event' : 'Setup New Event' }}</h3>
        <p class="modal-subtitle">Define the event details and scoring parameters.</p>
      </div>

      <div class="modal-form-body">
        <div class="form-group">
          <label>Event / Sport Name</label>
          <input v-model="form.name" type="text" class="modal-input" placeholder="e.g. Men's Basketball">
        </div>

        <div class="form-row">
          <div class="form-group flex-1">
            <label>Category</label>
            <select v-model="form.category" class="modal-input">
              <option v-for="cat in categories.slice(1)" :key="cat" :value="cat">{{ cat }}</option>
              <option value="Custom">Other (User Defined)</option>
            </select>
          </div>
          <div class="form-group flex-1" v-if="form.category === 'Custom'">
            <label>Specify Custom Category</label>
            <input v-model="form.customCategory" type="text" class="modal-input" placeholder="Enter type...">
          </div>
        </div>

        <div class="form-group">
          <label>Scoring System</label>
          <select v-model="form.scoringSystemId" class="modal-input">
            <option value="" disabled>Select a scoring system...</option>
            <option v-for="system in scoringSystems" :key="system.id" :value="system.id">
              {{ system.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Matchup System</label>
          <div class="toggle-group">
            <button
              type="button"
              :class="['toggle-btn', { active: form.matchupSystem === '1v1' }]"
              @click="form.matchupSystem = '1v1'"
            >
              <i class="fas fa-versus"></i> 1v1 (Head-to-Head)
            </button>
            <button
              type="button"
              :class="['toggle-btn', { active: form.matchupSystem === 'free-for-all' }]"
              @click="form.matchupSystem = 'free-for-all'"
            >
              <i class="fas fa-users"></i> Free-for-All
            </button>
          </div>
        </div>

        <div class="form-group">
          <div class="checkbox-label">
            <label class="checkbox-container">
              <input type="checkbox" v-model="form.thresholdIncremental">
              <span class="checkmark"></span>
              <span class="checkbox-text">Threshold Incremental (Set-based)</span>
            </label>
          </div>
        </div>

        <div v-if="form.thresholdIncremental" class="form-group">
          <label>Number of Sets</label>
          <input v-model.number="form.sets" type="number" class="modal-input" placeholder="e.g. 3" min="1">
          <small class="form-hint">Total sets to be played (e.g., 3 means best of 3)</small>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn-ghost" @click="emit('close')">Cancel</button>
        <button class="btn-primary" @click="handleSave">Save Event</button>
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
  max-width: 550px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
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

.form-row {
  display: flex;
  gap: 15px;
}

.flex-1 {
  flex: 1;
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

.form-hint {
  display: block;
  margin-top: 6px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* Toggle Group */
.toggle-group {
  display: flex;
  gap: 10px;
}

.toggle-btn {
  flex: 1;
  padding: 12px 16px;
  background: var(--bg-gray-light);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.2s;
  font-family: var(--font-main);
}

.toggle-btn.active {
  background: var(--adnu-blue-dark);
  color: var(--white);
  border-color: var(--adnu-blue-dark);
}

.toggle-btn:hover:not(.active) {
  background: var(--adnu-blue-light);
  border-color: var(--adnu-blue-dark);
}

/* Checkbox */
.checkbox-label {
  margin-bottom: 0;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: relative;
  height: 20px;
  width: 20px;
  background-color: var(--white);
  border: 2px solid var(--border-color);
  border-radius: 4px;
  margin-right: 12px;
  transition: all 0.2s;
}

.checkbox-container:hover input ~ .checkmark {
  border-color: var(--adnu-blue-dark);
}

.checkbox-container input:checked ~ .checkmark {
  background-color: var(--adnu-blue-dark);
  border-color: var(--adnu-blue-dark);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-text {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-main);
}

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
