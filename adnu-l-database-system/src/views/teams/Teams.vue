<script setup>
import { ref, reactive, computed } from 'vue';
import PageHeader from '../../components/common/PageHeader.vue';
import BaseModal from '../../components/modals/BaseModal.vue';
import { useStore } from '../../composables/useStore';
import { useAuth } from '../../composables/useAuth';

const { userRole } = useAuth();
const isAdmin = computed(() => userRole.value === 'admin');

const { state, addTeam, updateTeam, deleteTeam, toggleTeamSportParticipation } = useStore();

const showModal = ref(false);
const showParticipationModal = ref(false);
const isEditing = ref(false);
const editIndex = ref(null);
const selectedTeamForParticipation = ref(null);

const form = reactive({ name: '', color: '#0038A8' });

const openTeamModal = (team = null) => {
  if (team) {
    isEditing.value = true;
    editIndex.value = team.id;
    form.name = team.name;
    form.color = team.color;
  } else {
    isEditing.value = false;
    form.name = '';
    form.color = '#0038A8';
  }
  showModal.value = true;
};

const openParticipationModal = (team) => {
  selectedTeamForParticipation.value = team;
  showParticipationModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  showParticipationModal.value = false;
  selectedTeamForParticipation.value = null;
};

const saveTeam = () => {
  if (!form.name.trim()) {
    alert("Please enter a team name.");
    return;
  }
  if (isEditing.value) {
    updateTeam(editIndex.value, { name: form.name, color: form.color });
  } else {
    addTeam({ name: form.name, color: form.color });
  }
  closeModal();
};

const deleteTeamHandler = (id) => {
  const team = state.teams.find(t => t.id === id);
  if (confirm(`Are you sure you want to remove ${team?.name}?`)) {
    deleteTeam(id);
  }
};

const toggleParticipation = (sportId) => {
  if (selectedTeamForParticipation.value) {
    toggleTeamSportParticipation(selectedTeamForParticipation.value.id, sportId);
  }
};

const isParticipating = (teamId, sportId) => {
  const team = state.teams.find(t => t.id === teamId);
  return team?.participatingSports?.includes(sportId) || false;
};
</script>

<template>
  <div class="page-container">
    <PageHeader
      title="Teams Management"
      subtitle="Manage participating colleges and their representative colors."
    >
      <template #actions>
        <button v-if="isAdmin" class="btn-primary" @click="openTeamModal()">
          <i class="fas fa-plus"></i> Register New Team
        </button>
      </template>
    </PageHeader>

    <div class="teams-summary">
      <div class="summary-item">
        <span class="label">Total Teams</span>
        <span class="value">{{ state.teams.length }}</span>
      </div>
      <div class="summary-divider"></div>
      <div class="summary-item">
        <span class="label">Active Colleges</span>
        <span class="value">{{ state.teams.length }}</span>
      </div>
    </div>

    <div class="teams-grid">
      <div v-for="team in state.teams" :key="team.id" class="team-card">
        <div class="card-accent" :style="{ backgroundColor: team.color }"></div>
        <div class="team-card-body">
          <div class="team-icon" :style="{ color: team.color, backgroundColor: team.color + '15' }">
            <i class="fas fa-shield-alt"></i>
          </div>
          <div class="team-info">
            <h3>{{ team.name }}</h3>
            <p class="participation-count">
              <i class="fas fa-trophy"></i>
              Participating in {{ team.participatingSports?.length || 0 }} sports
            </p>
          </div>
        </div>
        <div class="team-card-actions">
          <button v-if="isAdmin" class="btn-icon participation" @click="openParticipationModal(team)" title="Manage Sport Participation">
            <i class="fas fa-clipboard-check"></i>
          </button>
          <button v-if="isAdmin" class="btn-icon edit" @click="openTeamModal(team)"><i class="fas fa-edit"></i></button>
          <button v-if="isAdmin" class="btn-icon delete" @click="deleteTeamHandler(team.id)"><i class="fas fa-trash-alt"></i></button>
        </div>
      </div>
    </div>

    <!-- Team Modal -->
    <BaseModal :show="showModal" @close="closeModal">
      <div class="modal-header-section">
        <h3>{{ isEditing ? 'Edit Team' : 'Register New Team' }}</h3>
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
        <button class="btn-ghost" @click="closeModal">Cancel</button>
        <button class="btn-primary" @click="saveTeam">Save changes</button>
      </div>
    </BaseModal>

    <!-- Sport Participation Modal -->
    <div v-if="showParticipationModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content participation-modal">
        <div class="modal-header-section">
          <h3>Sport Participation</h3>
          <p class="modal-subtitle">
            Select which sports <strong>{{ selectedTeamForParticipation?.name }}</strong> will participate in.
          </p>
        </div>

        <div class="participation-grid">
          <div
            v-for="event in state.events"
            :key="event.id"
            :class="['sport-card', { selected: isParticipating(selectedTeamForParticipation?.id, event.id) }]"
            @click="toggleParticipation(event.id)"
          >
            <div class="sport-card-header">
              <span class="sport-name">{{ event.name }}</span>
              <span class="sport-category">{{ event.category }}</span>
            </div>
            <div class="sport-card-footer">
              <span class="matchup-badge">{{ event.matchupSystem === '1v1' ? '1v1' : 'FFA' }}</span>
              <i :class="['participation-check', 'fas', isParticipating(selectedTeamForParticipation?.id, event.id) ? 'fa-check-circle' : 'fa-circle']"></i>
            </div>
          </div>
          <div v-if="state.events.length === 0" class="no-events">
            <i class="fas fa-inbox"></i>
            <p>No events configured yet. Create events first.</p>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-ghost" @click="closeModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  padding: 30px;
}

/* Teams Summary Card */
.teams-summary {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 20px 30px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  margin-bottom: 30px;
  width: fit-content;
}

.summary-item .label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
}

.summary-item .value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--adnu-blue-dark);
  display: block;
}

.summary-divider {
  width: 1px;
  height: 30px;
  background: var(--border-color);
  margin: 0 30px;
}

/* Grid & Cards */
.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.team-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.card-accent {
  height: 5px;
  width: 100%;
}

.team-card-body {
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.team-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.team-info h3 {
  margin: 0 0 6px 0;
  font-size: 1.1rem;
  color: var(--text-main);
  font-weight: 700;
}

.team-info p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.participation-count {
  display: flex;
  align-items: center;
  gap: 6px;
}

.participation-count i {
  font-size: 0.75rem;
  color: var(--adnu-gold);
}

.team-card-actions {
  border-top: 1px solid var(--border-color);
  padding: 12px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background: #fafafa;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 8px;
  border-radius: var(--radius-md);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: var(--bg-gray-light);
}

.btn-icon.edit:hover {
  color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
}

.btn-icon.delete:hover {
  color: var(--adnu-danger);
  background: var(--adnu-danger-light);
}

.btn-icon.participation:hover {
  color: var(--adnu-gold);
  background: #FFF9E6;
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

/* Participation Modal */
.participation-modal {
  max-width: 700px;
  border-top: 6px solid var(--adnu-gold);
}

.participation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  padding: 0 24px 24px 24px;
  max-height: 400px;
  overflow-y: auto;
}

.sport-card {
  padding: 16px;
  background: var(--bg-gray-light);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.sport-card:hover {
  border-color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
}

.sport-card.selected {
  border-color: var(--adnu-gold);
  background: #FFF9E6;
}

.sport-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.sport-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--adnu-blue-navy);
}

.sport-category {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--text-muted);
  background: var(--white);
  padding: 3px 8px;
  border-radius: 4px;
}

.sport-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.matchup-badge {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--white);
  padding: 3px 8px;
  border-radius: 4px;
}

.participation-check {
  font-size: 1.2rem;
}

.sport-card.selected .participation-check {
  color: var(--adnu-gold);
}

.no-events {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
}

.no-events i {
  font-size: 3rem;
  display: block;
  margin-bottom: 12px;
}

.no-events p {
  margin: 0;
  font-size: 0.95rem;
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
  max-width: 450px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
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

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
