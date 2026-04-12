<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from '../../composables/useStore';
import { useAuth } from '../../composables/useAuth';

const { userRole } = useAuth();
const isAdmin = computed(() => userRole.value === 'admin');

const { state, addEvent, updateEvent, deleteEvent, addScoringSystem, fetchEvents } = useStore();

// Fetch data on mount
onMounted(async () => {
  await fetchEvents();
});

const activeFilter = ref('All');

const showModal = ref(false);
const showScoringModal = ref(false);
const showCriteriaModal = ref(false);
const isEditing = ref(false);
const editIndex = ref(null);

const form = reactive({
  name: '',
  category: 'Sports',
  scoringSystemId: null,
  matchupSystem: '1v1',
  sets: null,
  criteria: []
});

const scoringForm = reactive({
  name: '',
  description: '',
  type: 'predefined'
});

const criteriaForm = reactive({
  criteriaList: [],
  newCriteriaName: '',
  newCriteriaPoints: null
});

const filteredEvents = computed(() => {
  if (activeFilter.value === 'All') return state.events;
  return state.events.filter(e => e.category === activeFilter.value);
});

const selectedScoringSystem = computed(() => {
  return state.scoringSystems.find(s => s.id === form.scoringSystemId);
});

const criteriaTotal = computed(() => {
  return form.criteria.reduce((sum, c) => sum + c.points, 0);
});

const openEventModal = (event = null) => {
  if (event) {
    isEditing.value = true;
    editIndex.value = event.id;
    form.name = event.name;
    form.category = event.category;
    form.scoringSystemId = event.scoringSystemId;
    form.matchupSystem = event.matchupSystem || '1v1';
    form.sets = event.sets || null;
    form.criteria = event.criteria ? JSON.parse(JSON.stringify(event.criteria)) : [];
  } else {
    isEditing.value = false;
    form.name = '';
    form.category = 'Sports';
    form.scoringSystemId = null;
    form.matchupSystem = '1v1';
    form.sets = null;
    form.criteria = [];
  }
  showModal.value = true;
};

const openScoringModal = () => {
  scoringForm.name = '';
  scoringForm.description = '';
  scoringForm.type = 'predefined';
  showScoringModal.value = true;
};

const openCriteriaModal = () => {
  criteriaForm.criteriaList = form.criteria.length > 0
    ? form.criteria.map(c => ({ ...c }))
    : [];
  criteriaForm.newCriteriaName = '';
  criteriaForm.newCriteriaPoints = null;
  showCriteriaModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  showScoringModal.value = false;
  showCriteriaModal.value = false;
};

const addCriteria = () => {
  if (!criteriaForm.newCriteriaName.trim()) {
    alert('Please enter a criteria name');
    return;
  }
  if (!criteriaForm.newCriteriaPoints || criteriaForm.newCriteriaPoints <= 0) {
    alert('Please enter a valid point value (greater than 0)');
    return;
  }
  criteriaForm.criteriaList.push({
    name: criteriaForm.newCriteriaName,
    points: criteriaForm.newCriteriaPoints
  });
  criteriaForm.newCriteriaName = '';
  criteriaForm.newCriteriaPoints = null;
};

const removeCriteria = (index) => {
  criteriaForm.criteriaList.splice(index, 1);
};

const saveCriteria = () => {
  const total = criteriaForm.criteriaList.reduce((sum, c) => sum + c.points, 0);
  if (total !== 100) {
    alert(`Total criteria points must equal 100. Current total: ${total}`);
    return;
  }
  if (criteriaForm.criteriaList.length === 0) {
    alert('Please add at least one criteria');
    return;
  }
  form.criteria = criteriaForm.criteriaList.map(c => ({ ...c }));
  showCriteriaModal.value = false;
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

  const selectedSystem = state.scoringSystems.find(s => s.id === form.scoringSystemId);

  // Validate sets for Threshold Incremental
  if (selectedSystem?.requiresSets) {
    if (!form.sets || form.sets < 1) {
      alert('Please enter a valid number of sets');
      return;
    }
  }

  // Validate criteria for Criteria Based and Judge Based
  if (selectedSystem?.requiresCriteria) {
    if (form.criteria.length === 0) {
      alert('Please add criteria/rubrics for this scoring system');
      return;
    }
    const total = form.criteria.reduce((sum, c) => sum + c.points, 0);
    if (total !== 100) {
      alert(`Total criteria points must equal 100. Current total: ${total}`);
      return;
    }
  }

  const eventData = {
    name: form.name,
    category: form.category,
    scoringSystemId: form.scoringSystemId,
    matchupSystem: form.matchupSystem,
    sets: selectedSystem?.requiresSets ? form.sets : null,
    criteria: selectedSystem?.requiresCriteria ? form.criteria : []
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

const getCategoryClass = (category) => {
  const classMap = {
    'Sports': 'sports',
    'Special Events': 'special-events',
    'Esports': 'esports',
    'Board Games': 'board-games',
    'Laro ng Lahi': 'laro-ng-lahi',
    'LitMusDa': 'litmusda',
    'Outside Events': 'outside-events',
    'Indoor Games': 'indoor-games'
  };
  return classMap[category] || 'default';
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
        :class="['filter-btn', { active: activeFilter === 'All' }]"
        @click="activeFilter = 'All'"
      >
        All
      </button>
      <button
        v-for="cat in state.eventCategories"
        :key="cat"
        :class="['filter-btn', { active: activeFilter === cat }]"
        @click="activeFilter = cat"
      >
        {{ cat }}
      </button>
    </div>

    <div class="events-grid">
      <div v-for="event in filteredEvents" :key="event.id" class="event-card">
        <div class="event-type-tag" :class="getCategoryClass(event.category)">
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
              <span v-if="event.sets" class="detail-badge">
                <i class="fas fa-layer-group"></i>
                {{ event.sets }} Sets
              </span>
              <span v-if="event.criteria && event.criteria.length > 0" class="detail-badge">
                <i class="fas fa-list-check"></i>
                {{ event.criteria.length }} Criteria
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

          <div class="form-group">
            <label>Category</label>
            <select v-model="form.category" class="modal-input">
              <option v-for="cat in state.eventCategories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
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

          <!-- Sets configuration for Threshold Incremental -->
          <div v-if="selectedScoringSystem?.requiresSets" class="form-group">
            <label>Number of Sets</label>
            <input v-model.number="form.sets" type="number" class="modal-input" placeholder="e.g. 3" min="1">
            <small class="form-hint">Total sets to be played (e.g., 3 means best of 3)</small>
          </div>

          <!-- Criteria configuration for Criteria Based and Judge Based -->
          <div v-if="selectedScoringSystem?.requiresCriteria" class="form-group">
            <label>Criteria / Rubrics</label>
            <div class="criteria-config">
              <div v-if="form.criteria.length > 0" class="criteria-list">
                <div v-for="(criteria, idx) in form.criteria" :key="idx" class="criteria-item">
                  <span class="criteria-name">{{ criteria.name }}</span>
                  <span class="criteria-points">{{ criteria.points }} pts</span>
                </div>
                <div class="criteria-total" :class="{ 'invalid': criteriaTotal !== 100 }">
                  Total: {{ criteriaTotal }} / 100
                </div>
              </div>
              <button type="button" class="btn-manage-criteria" @click="openCriteriaModal">
                <i class="fas fa-cog"></i> {{ form.criteria.length > 0 ? 'Manage Criteria' : 'Add Criteria' }}
              </button>
            </div>
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

    <!-- Criteria Modal -->
    <div v-if="showCriteriaModal" class="modal-overlay" @click.self="showCriteriaModal = false">
      <div class="modal-content criteria-modal">
        <div class="modal-header-section">
          <h3>Manage Criteria / Rubrics</h3>
          <p class="modal-subtitle">Add criteria with point values. Total must equal exactly 100 points.</p>
        </div>

        <div class="modal-form-body">
          <div class="criteria-input-section">
            <div class="form-row criteria-input-row">
              <div class="form-group flex-2">
                <label>Criteria Name</label>
                <input v-model="criteriaForm.newCriteriaName" type="text" class="modal-input" placeholder="e.g. Stage Presence">
              </div>
              <div class="form-group flex-1">
                <label>Points</label>
                <input v-model.number="criteriaForm.newCriteriaPoints" type="number" class="modal-input" placeholder="0" min="1">
              </div>
            </div>
            <button type="button" class="btn-add-criteria" @click="addCriteria">
              <i class="fas fa-plus"></i> Add Criteria
            </button>
          </div>

          <div class="criteria-list-section">
            <h4>Added Criteria</h4>
            <div v-if="criteriaForm.criteriaList.length === 0" class="no-criteria">
              <i class="fas fa-list-ul"></i>
              <p>No criteria added yet. Add criteria above.</p>
            </div>
            <div v-else class="criteria-list">
              <div v-for="(criteria, idx) in criteriaForm.criteriaList" :key="idx" class="criteria-item">
                <span class="criteria-name">{{ criteria.name }}</span>
                <span class="criteria-points">{{ criteria.points }} pts</span>
                <button type="button" class="btn-remove-criteria" @click="removeCriteria(idx)">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
            <div class="criteria-total-display" :class="{ 'invalid': criteriaForm.criteriaList.reduce((sum, c) => sum + c.points, 0) !== 100 }">
              <strong>Total:</strong> {{ criteriaForm.criteriaList.reduce((sum, c) => sum + c.points, 0) }} / 100
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-ghost" @click="showCriteriaModal = false">Cancel</button>
          <button class="btn-primary" @click="saveCriteria">
            <i class="fas fa-check"></i> Save Criteria
          </button>
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
.event-type-tag.special-events { background: #F3E8FF; color: #7C3AED; }
.event-type-tag.esports { background: #1A1A2E; color: #00D9FF; }
.event-type-tag.board-games { background: #FFF5E6; color: #D97706; }
.event-type-tag.laro-ng-lahi { background: #FFF3E0; color: #E65100; }
.event-type-tag.litmusda { background: #FCE7F3; color: #DB2777; }
.event-type-tag.outside-events { background: #D1FAE5; color: #059669; }
.event-type-tag.indoor-games { background: #E0E7FF; color: #4F46E5; }
.event-type-tag.default { background: #F3F4F6; color: #374151; }

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

/* Criteria Configuration */
.criteria-config {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: var(--bg-gray-light);
  border-radius: var(--radius-md);
}

.criteria-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--white);
  border-radius: 4px;
}

.criteria-name {
  font-weight: 600;
  color: var(--text-main);
}

.criteria-points {
  font-weight: 700;
  color: var(--adnu-blue-dark);
}

.criteria-total {
  margin-top: 8px;
  padding: 8px 12px;
  background: var(--adnu-blue-light);
  border-radius: 4px;
  font-weight: 700;
  color: var(--adnu-blue-navy);
  text-align: right;
}

.criteria-total.invalid {
  background: var(--adnu-danger-light);
  color: var(--adnu-danger);
}

.btn-manage-criteria {
  padding: 10px 16px;
  background: var(--bg-gray-light);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  color: var(--adnu-blue-dark);
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-manage-criteria:hover {
  background: var(--adnu-blue-light);
  border-color: var(--adnu-blue-dark);
}

/* Criteria Modal */
.criteria-modal {
  max-width: 550px;
  border-top: 6px solid var(--adnu-gold);
}

.criteria-input-section {
  margin-bottom: 20px;
}

.criteria-input-row {
  align-items: flex-end;
}

.flex-2 {
  flex: 2;
}

.btn-add-criteria {
  margin-top: 10px;
  padding: 10px 16px;
  background: var(--adnu-blue-dark);
  color: var(--white);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-add-criteria:hover {
  background: var(--adnu-blue-navy);
}

.criteria-list-section h4 {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--adnu-blue-navy);
  text-transform: uppercase;
  margin: 0 0 12px 0;
}

.no-criteria {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 20px;
  color: var(--text-muted);
  background: var(--bg-gray-light);
  border-radius: var(--radius-md);
}

.no-criteria i {
  font-size: 2.5rem;
  opacity: 0.5;
}

.no-criteria p {
  margin: 0;
  font-size: 0.9rem;
}

.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.criteria-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--bg-gray-light);
  border-radius: var(--radius-md);
}

.btn-remove-criteria {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--white);
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-remove-criteria:hover {
  background: var(--adnu-danger-light);
  border-color: var(--adnu-danger);
  color: var(--adnu-danger);
}

.criteria-total-display {
  padding: 12px 16px;
  background: var(--adnu-blue-light);
  border-radius: var(--radius-md);
  font-weight: 700;
  color: var(--adnu-blue-navy);
  text-align: right;
  font-size: 1.05rem;
}

.criteria-total-display.invalid {
  background: var(--adnu-danger-light);
  color: var(--adnu-danger);
}

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
