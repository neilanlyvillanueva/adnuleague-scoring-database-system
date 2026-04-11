<script setup>
import { ref, reactive, computed } from 'vue';
import { useStore } from '../../composables/useStore';
import EventsList from '../../components/sections/EventsList.vue';
import EventModal from '../../components/modals/EventModal.vue';
import ScoringSystemModal from '../../components/modals/ScoringSystemModal.vue';

const { state, addEvent, updateEvent, deleteEvent, addScoringSystem } = useStore();

const categories = ['All', 'Sports', 'Cultural', 'Academic', 'Laro ng Lahi'];
const activeFilter = ref('All');

const showModal = ref(false);
const showScoringModal = ref(false);
const editingEvent = ref(null);
const selectedScoringSystemId = ref(null);

const scoringForm = reactive({
  name: '',
  description: ''
});

const filteredEvents = computed(() => {
  if (activeFilter.value === 'All') return state.events;
  return state.events.filter(e => e.category === activeFilter.value);
});

const openEventModal = (event = null) => {
  editingEvent.value = event;
  showModal.value = true;
};

const openScoringModal = () => {
  scoringForm.name = '';
  scoringForm.description = '';
  showScoringModal.value = true;
};

const handleSaveEvent = (eventData) => {
  if (!eventData.name.trim()) {
    alert('Please enter an event name');
    return;
  }
  if (!eventData.scoringSystemId) {
    alert('Please select a scoring system');
    return;
  }

  if (editingEvent.value) {
    updateEvent(editingEvent.value.id, eventData);
  } else {
    addEvent(eventData);
  }

  showModal.value = false;
  editingEvent.value = null;
};

const deleteEventHandler = (id) => {
  if (confirm("Delete this event?")) {
    deleteEvent(id);
  }
};

const handleSelectScoringSystem = (systemId) => {
  selectedScoringSystemId.value = systemId;
};

const handleAddCustomScoring = (systemData) => {
  addScoringSystem(systemData);
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
        <button class="btn-ghost" @click="openScoringModal()">
          <i class="fas fa-cog"></i> Manage Scoring
        </button>
        <button class="btn-primary" @click="openEventModal()">
          <i class="fas fa-plus"></i> Create New Event
        </button>
      </div>
    </header>

    <EventsList
      :events="filteredEvents"
      :scoring-systems="state.scoringSystems"
      :active-filter="activeFilter"
      :categories="categories"
      @filter-change="activeFilter = $event"
      @edit-event="openEventModal"
      @delete-event="deleteEventHandler"
    />

    <!-- Event Modal -->
    <EventModal
      :show="showModal"
      :event="editingEvent"
      :scoring-systems="state.scoringSystems"
      :categories="categories"
      @close="showModal = false; editingEvent = null"
      @save="handleSaveEvent"
    />

    <!-- Scoring System Modal -->
    <ScoringSystemModal
      :show="showScoringModal"
      :scoring-systems="state.scoringSystems"
      :selected-system-id="selectedScoringSystemId"
      @close="showScoringModal = false"
      @select="handleSelectScoringSystem"
      @add-custom="handleAddCustomScoring"
    />
  </div>
</template>

<style scoped>
.page-container { padding: 30px; }
</style>
