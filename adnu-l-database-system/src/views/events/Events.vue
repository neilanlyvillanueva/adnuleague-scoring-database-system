<script setup>
import { ref, reactive, computed } from 'vue';
import { useStore } from '../../composables/useStore';
import { useAuth } from '../../composables/useAuth';

const { userRole } = useAuth();
const isAdmin = computed(() => userRole.value === 'admin');

const { state, addEvent, updateEvent, deleteEvent, addScoringSystem } = useStore();

const categories = ['All', 'Sports', 'Cultural', 'Academic', 'Laro ng Lahi'];
const activeFilter = ref('All');

const showModal = ref(false);
const showScoringModal = ref(false);
const isEditing = ref(false);
const editIndex = ref(null);

const form = reactive({
  name: '',
  category: 'Sports',
  customCategory: '',
  scoringSystemId: null,
  thresholdIncremental: false,
  sets: null,
  matchupSystem: '1v1'
});

const scoringForm = reactive({
  name: '',
  description: '',
  type: 'predefined'
});

const filteredEvents = computed(() => {
  if (activeFilter.value === 'All') return state.events;
  return state.events.filter(e => e.category === activeFilter.value);
});

const openEventModal = (event = null) => {
  if (event) {
    isEditing.value = true;
    editIndex.value = event.id;
    form.name = event.name;
    form.category = event.category;
    form.customCategory = '';
    form.scoringSystemId = event.scoringSystemId;
    form.thresholdIncremental = event.thresholdIncremental;
    form.sets = event.sets;
    form.matchupSystem = event.matchupSystem;
  } else {
    isEditing.value = false;
    form.name = '';
    form.category = 'Sports';
    form.customCategory = '';
    form.scoringSystemId = null;
    form.thresholdIncremental = false;
    form.sets = null;
    form.matchupSystem = '1v1';
  }
  showModal.value = true;
};

const openScoringModal = () => {
  scoringForm.name = '';
  scoringForm.description = '';
  scoringForm.type = 'predefined';
  showScoringModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  showScoringModal.value = false;
};

const saveEvent = () => {
  if (!form.name.trim()) {
    alert('Please enter an event name');
    return;
  }
  if (!form.scoringSystemId) {
    alert('Please select a scoring system');
    return;
  }

  const finalCategory = form.category === 'Custom' ? form.customCategory : form.category;
  const eventData = {
    name: form.name,
    category: finalCategory,
    scoringSystemId: form.scoringSystemId,
    thresholdIncremental: form.thresholdIncremental,
    sets: form.thresholdIncremental ? form.sets : null,
    matchupSystem: form.matchupSystem
  };

  if (isEditing.value) {
    updateEvent(editIndex.value, eventData);
  } else {
    addEvent(eventData);
  }

  closeModal();
};

const deleteEventHandler = (id) => {
  if (confirm("Delete this event?")) {
    deleteEvent(id);
  }
};

const saveScoringSystem = () => {
  if (!scoringForm.name.trim()) {
    alert('Please enter a scoring system name');
    return;
  }
  addScoringSystem({
    name: scoringForm.name,
    description: scoringForm.description
  });
  showScoringModal.value = false;
};
</script>

<template>
<div class="page-container">
    <header class="dashboard-header">
      <div class="welcome-text">
        <h1>Events Management</h1>
        <p>Organize competition categories and specific contest rules.</p>
      </div>
      <div class="header-actions">
        <button v-if="isAdmin" class="btn-ghost" @click="openScoringModal()">
          <i class="fas fa-cog"></i> Manage Scoring
        </button>
        <button v-if="isAdmin" class="btn-primary" @click="openEventModal()">
          <i class="fas fa-plus"></i> Create New Event
        </button>
      </div>
    </header>

    <div class="filter-bar">
      <button
        v-for="cat in categories"
        :key="cat"
        :class="['filter-btn', { active: activeFilter === cat }]"
        @click="activeFilter = cat"
      >
        {{ cat }}
      </button>
    </div>

    <div class="events-grid">
      <div v-for="event in filteredEvents" :key="event.id" class="event-card">
        <div class="event-type-tag" :class="event.category.toLowerCase().replace(/\s+/g, '-')">
          {{ event.category }}
        </div>
        <div class="event-card-content">
          <div class="event-main">
            <h3>{{ event.name }}</h3>
            <div class="event-details">
              <span class="detail-badge">
                <i class="fas fa-trophy"></i>
                {{ state.scoringSystems.find(s => s.id === event.scoringSystemId)?.name || 'Unknown' }}
              </span>
              <span v-if="event.matchupSystem" class="detail-badge">
                <i class="fas fa-users"></i>
                {{ event.matchupSystem === '1v1' ? 'Head-to-Head' : 'Free-for-All' }}
              </span>
              <span v-if="event.thresholdIncremental" class="detail-badge">
                <i class="fas fa-layer-group"></i>
                {{ event.sets }} Sets
              </span>
            </div>
          </div>
          <div class="event-footer">
            <div class="action-group">
              <button v-if="isAdmin" class="btn-icon edit" @click="openEventModal(event)"><i class="fas fa-edit"></i></button>
              <button v-if="isAdmin" class="btn-icon delete" @click="deleteEventHandler(event.id)"><i class="fas fa-trash-alt"></i></button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content event-modal">
        <div class="modal-header-section">
          <h3>{{ isEditing ? 'Edit Event' : 'Setup New Event' }}</h3>
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
            <div class="scoring-system-select">
              <select v-model="form.scoringSystemId" class="modal-input">
                <option value="" disabled>Select a scoring system...</option>
                <option v-for="system in state.scoringSystems" :key="system.id" :value="system.id">
                  {{ system.name }}
                </option>
              </select>
              <button type="button" class="btn-add-scoring" @click="openScoringModal">
                <i class="fas fa-plus"></i> Add New
              </button>
            </div>
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
          <button class="btn-ghost" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveEvent">Save Event</button>
        </div>
      </div>
    </div>

    <!-- Scoring System Modal -->
    <div v-if="showScoringModal" class="modal-overlay" @click.self="showScoringModal = false">
      <div class="modal-content scoring-modal">
        <div class="modal-header-section">
          <h3>Manage Scoring Systems</h3>
          <p class="modal-subtitle">Choose from pre-defined systems or create a custom one.</p>
        </div>

        <div class="scoring-systems-list">
          <h4>Pre-defined Systems</h4>
          <div class="scoring-systems-grid">
            <div
              v-for="system in state.scoringSystems.filter(s => s.type === 'predefined')"
              :key="system.id"
              :class="['scoring-system-card', { selected: form.scoringSystemId === system.id }]"
            >
              <div class="scoring-system-info">
                <h5>{{ system.name }}</h5>
                <p>{{ system.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>Add Custom Scoring System</label>
          <input v-model="scoringForm.name" type="text" class="modal-input" placeholder="System name...">
          <input v-model="scoringForm.description" type="text" class="modal-input" placeholder="Description..." style="margin-top: 8px;">
        </div>

        <div class="modal-actions">
          <button class="btn-ghost" @click="showScoringModal = false">Close</button>
          <button class="btn-primary" @click="saveScoringSystem">Add Custom System</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container { padding: 30px; }

/* Dashboard Header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.welcome-text h1 {
  margin: 0 0 8px 0;
  font-size: 1.8rem;
  color: var(--adnu-blue-navy);
  font-weight: 700;
}

.welcome-text p {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .btn-primary,
.header-actions .btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

/* Filter Bar */
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  background: var(--white);
  color: var(--text-muted);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: var(--bg-gray-light);
  border-color: var(--adnu-blue-dark);
}

.filter-btn.active {
  background: var(--adnu-blue-dark);
  color: var(--white);
  border-color: var(--adnu-blue-dark);
}

/* Events Grid */
.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.event-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: box-shadow 0.2s ease;
}

.event-card:hover {
  box-shadow: var(--shadow-md);
}

.event-type-tag {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 8px 15px;
  letter-spacing: 0.5px;
}

.event-type-tag.sports { background: #E8F0FF; color: var(--adnu-blue-dark); }
.event-type-tag.cultural { background: #FFF9E6; color: #B8860B; }
.event-type-tag.academic { background: #E8F5E9; color: #2E7D32; }
.event-type-tag.laro-ng-lahi { background: #FFF3E0; color: #E65100; }

.event-card-content { padding: 20px; }

.event-main h3 {
  margin: 0 0 12px 0;
  font-size: 1.15rem;
  color: var(--adnu-blue-navy);
  font-weight: 700;
}

.event-details {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.detail-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--bg-gray-light);
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.detail-badge i {
  font-size: 0.75rem;
}

.event-footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid var(--border-color);
  padding-top: 12px;
}

.action-group {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--white);
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 0.85rem;
}

.btn-icon:hover {
  transform: translateY(-1px);
}

.btn-icon.edit:hover {
  background: var(--adnu-blue-light);
  border-color: var(--adnu-blue-dark);
  color: var(--adnu-blue-dark);
}

.btn-icon.delete:hover {
  background: var(--adnu-danger-light);
  border-color: var(--adnu-danger);
  color: var(--adnu-danger);
}

/* Modal Overlay */
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
}

.event-modal { max-width: 550px; border-top: 6px solid var(--adnu-gold); }
.scoring-modal { max-width: 600px; border-top: 6px solid var(--adnu-blue-dark); }

.modal-header-section { padding: 24px 24px 16px 24px; }

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

.modal-form-body { padding: 0 24px 24px 24px; }

.form-row { 
  display: flex; 
  gap: 15px; 
}

.flex-1 {
  flex: 1;
}

.form-group { 
  margin: 20px; 
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

/* Scoring System Select */
.scoring-system-select {
  display: flex;
  gap: 10px;
}

.scoring-system-select .modal-input {
  flex: 1;
}

.btn-add-scoring {
  padding: 12px 16px;
  background: var(--bg-gray-light);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  color: var(--adnu-blue-dark);
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-add-scoring:hover {
  background: var(--adnu-blue-light);
  border-color: var(--adnu-blue-dark);
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
.checkbox-label { margin-bottom: 0; }

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

/* Scoring Systems List */
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

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
