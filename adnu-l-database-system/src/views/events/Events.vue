<script setup>
import { ref, reactive, computed } from 'vue';

const categories = ['All', 'Sports', 'Cultural', 'Academic', 'Laro ng Lahi'];
const activeFilter = ref('All');

const events = ref([
  { name: 'Men\'s Basketball', category: 'Sports', scoringMethod: 'Point-based (Win/Loss)', isLive: true },
  { name: 'Vocal Solo', category: 'Cultural', scoringMethod: 'Judged (Criteria)', isLive: false },
  { name: 'General Information Quiz', category: 'Academic', scoringMethod: 'Point-based (Win/Loss)', isLive: false }
]);

const showModal = ref(false);
const isEditing = ref(false);
const editIndex = ref(null);

const form = reactive({
  name: '',
  category: 'Sports',
  customCategory: '',
  scoringMethod: 'Point-based (Win/Loss)'
});

const filteredEvents = computed(() => {
  if (activeFilter.value === 'All') return events.value;
  return events.value.filter(e => e.category === activeFilter.value);
});

const openEventModal = (index = null) => {
  if (index !== null) {
    isEditing.value = true;
    editIndex.value = index;
    Object.assign(form, events.value[index]);
  } else {
    isEditing.value = false;
    form.name = '';
    form.category = 'Sports';
    form.customCategory = '';
  }
  showModal.value = true;
};

const closeModal = () => { showModal.value = false; };

const saveEvent = () => {
  const finalCategory = form.category === 'Custom' ? form.customCategory : form.category;
  const eventData = { ...form, category: finalCategory, isLive: false };
  
  if (isEditing.value) events.value[editIndex.value] = eventData;
  else events.value.push(eventData);
  
  closeModal();
};

const deleteEvent = (index) => {
  if (confirm("Delete this event?")) events.value.splice(index, 1);
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
        <button class="btn-primary" @click="openEventModal()">
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
      <div v-for="(event, index) in filteredEvents" :key="index" class="event-card">
        <div class="event-type-tag" :class="event.category.toLowerCase()">
          {{ event.category }}
        </div>
        <div class="event-card-content">
          <div class="event-main">
            <h3>{{ event.name }}</h3>
            <span class="scoring-type">Method: {{ event.scoringMethod }}</span>
          </div>
          <div class="event-footer">
            <span class="status-indicator" :class="{ active: event.isLive }">
              <i class="fas fa-circle"></i> {{ event.isLive ? 'Live' : 'Pending' }}
            </span>
            <div class="action-group">
              <button class="btn-icon edit" @click="openEventModal(index)"><i class="fas fa-edit"></i></button>
              <button class="btn-icon delete" @click="deleteEvent(index)"><i class="fas fa-trash-alt"></i></button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content event-modal">
        <div class="modal-header-section">
          <h3>{{ isEditing ? 'Edit Event' : 'Setup New Event' }}</h3>
          <p class="modal-subtitle">Define the event details and scoring parameters.</p>
        </div>

        <div class="modal-form-body">
          <div class="form-group">
            <label>Event Name</label>
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
            <label>Scoring Method</label>
            <select v-model="form.scoringMethod" class="modal-input">
              <option value="Point-based (Win/Loss)">Point-based (Win/Loss)</option>
              <option value="Judged (Criteria)">Judged (Criteria / LitMusDa)</option>
              <option value="Timed (Race)">Timed (Race/Speed)</option>
            </select>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-ghost" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveEvent">Save Event</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container { padding: 30px; }

/* Filter Bar */
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 30px;
}

.filter-btn {
  padding: 8px 18px;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  background: var(--white);
  color: var(--text-muted);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.filter-btn.active {
  background: var(--adnu-blue-dark);
  color: var(--white);
  border-color: var(--adnu-blue-dark);
}

/* Events Grid */
.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.event-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.event-type-tag {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 6px 15px;
  background: #f0f0f0;
  color: #666;
}

.event-type-tag.sports { 
    background: #E8F0FF; 
    color: var(--adnu-blue-dark); 
}

.event-type-tag.cultural { 
    background: #FFF9E6; 
    color: var(--adnu-gold); 
}

.event-card-content { 
    padding: 20px; 
}

.event-main h3 { 
    margin: 0; 
    font-size: 1.2rem; 
    color: var(--adnu-blue-navy); 
}

.scoring-type { 
    font-size: 0.85rem; 
    color: var(--text-muted); 
    display: block; 
    margin-top: 5px; 
}

.event-footer {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
  padding-top: 15px;
}

.status-indicator { 
    font-size: 0.8rem; 
    font-weight: 600; 
    color: var(--text-muted); 
}

.status-indicator i { 
    font-size: 0.6rem; 
    margin-right: 5px; 
    color: #cbd5e0; 
}

.status-indicator.active i { 
    color: var(--adnu-live-red); 
}

.form-row { 
    display: flex; 
    gap: 15px; 
}

.flex-1 { 
    flex: 1; 
}

.event-modal { 
    width: 500px; 
    border-top: 6px solid var(--adnu-gold); 
}
</style>