<script setup>
import { reactive, watch, computed } from 'vue';

const props = defineProps({
  show: Boolean,
  match: Object,
  events: Array,
  teams: Array
});

const emit = defineEmits(['close', 'save']);

const form = reactive({
  eventId: null,
  matchupType: '1v1',
  teamAId: null,
  teamBId: null,
  participants: [],
  venue: ''
});

// Get teams participating in a specific event
const getParticipatingTeams = computed(() => (eventId) => {
  return props.teams.filter(t => t.participatingSports?.includes(eventId));
});

watch(() => props.match, (newMatch) => {
  if (newMatch) {
    form.eventId = newMatch.eventId;
    form.matchupType = newMatch.matchupType;
    form.teamAId = newMatch.teamAId;
    form.teamBId = newMatch.teamBId;
    form.participants = newMatch.participants || [];
    form.venue = newMatch.venue || '';
  } else {
    form.eventId = null;
    form.matchupType = '1v1';
    form.teamAId = null;
    form.teamBId = null;
    form.participants = [];
    form.venue = '';
  }
}, { immediate: true });

const handleSave = () => {
  emit('save', { ...form });
};

const toggleParticipant = (teamId) => {
  const index = form.participants.indexOf(teamId);
  if (index === -1) {
    form.participants.push(teamId);
  } else {
    form.participants.splice(index, 1);
  }
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content match-modal">
      <div class="modal-header-section">
        <h3>{{ match ? 'Edit Match' : 'Create New Match' }}</h3>
        <p class="modal-subtitle">Set up the match details and participants.</p>
      </div>

      <div class="modal-form-body">
        <div class="form-group">
          <label>Select Event / Sport</label>
          <select v-model="form.eventId" class="modal-input">
            <option value="" disabled>Select an event...</option>
            <option v-for="event in events" :key="event.id" :value="event.id">
              {{ event.name }} ({{ event.matchupSystem }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Matchup Type</label>
          <div class="toggle-group">
            <button
              type="button"
              :class="['toggle-btn', { active: form.matchupType === '1v1' }]"
              @click="form.matchupType = '1v1'"
            >
              <i class="fas fa-versus"></i> 1v1 (Head-to-Head)
            </button>
            <button
              type="button"
              :class="['toggle-btn', { active: form.matchupType === 'free-for-all' }]"
              @click="form.matchupType = 'free-for-all'"
            >
              <i class="fas fa-users"></i> Free-for-All
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Venue</label>
          <input v-model="form.venue" type="text" class="modal-input" placeholder="e.g. Main Gymnasium">
        </div>

        <!-- Team Selection for 1v1 -->
        <div v-if="form.matchupType === '1v1' && form.eventId" class="team-selection">
          <div class="form-row">
            <div class="form-group flex-1">
              <label>Team A</label>
              <select v-model="form.teamAId" class="modal-input">
                <option value="" disabled>Select Team A...</option>
                <option v-for="team in getParticipatingTeams(form.eventId)"
                        :key="team.id" :value="team.id">
                  {{ team.name }}
                </option>
              </select>
            </div>
            <div class="form-group flex-1">
              <label>Team B</label>
              <select v-model="form.teamBId" class="modal-input">
                <option value="" disabled>Select Team B...</option>
                <option v-for="team in getParticipatingTeams(form.eventId)"
                        :key="team.id" :value="team.id">
                  {{ team.name }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Team Selection for Free-for-All -->
        <div v-if="form.matchupType === 'free-for-all' && form.eventId" class="team-selection">
          <label>Select Participants</label>
          <div class="participant-selectors">
            <div
              v-for="team in getParticipatingTeams(form.eventId)"
              :key="team.id"
              :class="['participant-option', { selected: form.participants.includes(team.id) }]"
              @click="toggleParticipant(team.id)"
            >
              <span class="team-dot" :style="{ backgroundColor: team.color }"></span>
              <span class="team-name">{{ team.name }}</span>
              <i :class="['fas', form.participants.includes(team.id) ? 'fa-check-circle' : 'fa-circle']"></i>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn-ghost" @click="emit('close')">Cancel</button>
        <button class="btn-primary" @click="handleSave">Create Match</button>
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

/* Team Selection */
.team-selection {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.participant-selectors {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 250px;
  overflow-y: auto;
}

.participant-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: var(--bg-gray-light);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.participant-option:hover {
  border-color: var(--adnu-blue-dark);
}

.participant-option.selected {
  border-color: var(--adnu-gold);
  background: #FFF9E6;
}

.team-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.participant-option .team-name {
  flex: 1;
  font-weight: 600;
  font-size: 0.95rem;
}

.participant-option i {
  font-size: 1rem;
}

.participant-option.selected i {
  color: var(--adnu-gold);
}

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
