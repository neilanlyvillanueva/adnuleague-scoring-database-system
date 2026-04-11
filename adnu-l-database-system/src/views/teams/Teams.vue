<script setup>
import { ref } from 'vue';
import { useStore } from '../../composables/useStore';
import PageHeader from '../../components/common/PageHeader.vue';
import TeamsList from '../../components/sections/TeamsList.vue';
import TeamModal from '../../components/modals/TeamModal.vue';
import ParticipationModal from '../../components/modals/ParticipationModal.vue';

const { state, addTeam, updateTeam, deleteTeam, toggleTeamSportParticipation } = useStore();

const showModal = ref(false);
const showParticipationModal = ref(false);
const editingTeam = ref(null);
const selectedTeamForParticipation = ref(null);

const openTeamModal = (team = null) => {
  editingTeam.value = team;
  showModal.value = true;
};

const openParticipationModal = (team) => {
  selectedTeamForParticipation.value = team;
  showParticipationModal.value = true;
};

const closeModals = () => {
  showModal.value = false;
  showParticipationModal.value = false;
  editingTeam.value = null;
  selectedTeamForParticipation.value = null;
};

const handleSaveTeam = (teamData) => {
  if (editingTeam.value) {
    updateTeam(editingTeam.value.id, teamData);
  } else {
    addTeam(teamData);
  }
  closeModals();
};

const deleteTeamHandler = (id) => {
  const team = state.teams.find(t => t.id === id);
  if (confirm(`Are you sure you want to remove ${team?.name}?`)) {
    deleteTeam(id);
  }
};

const handleToggleParticipation = (sportId) => {
  if (selectedTeamForParticipation.value) {
    toggleTeamSportParticipation(selectedTeamForParticipation.value.id, sportId);
  }
};
</script>

<template>
  <div class="page-container">
    <PageHeader
      title="Teams Management"
      subtitle="Manage participating colleges and their representative colors."
    >
      <template #actions>
        <button class="btn-primary" @click="openTeamModal()">
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

    <TeamsList
      :teams="state.teams"
      @edit-team="openTeamModal"
      @delete-team="deleteTeamHandler"
      @manage-participation="openParticipationModal"
    />

    <TeamModal
      :show="showModal"
      :team="editingTeam"
      @close="closeModals"
      @save="handleSaveTeam"
    />

    <ParticipationModal
      :show="showParticipationModal"
      :team="selectedTeamForParticipation"
      :events="state.events"
      :participating-sports="selectedTeamForParticipation?.participatingSports || []"
      @close="closeModals"
      @toggle-participation="handleToggleParticipation"
    />
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
</style>
