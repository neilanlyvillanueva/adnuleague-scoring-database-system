<script setup>
import { ref, reactive } from 'vue';
import PageHeader from '../../components/common/PageHeader.vue';
import BaseModal from '../../components/common/BaseModal.vue';

const teams = ref([
  { name: 'Business & Accountancy', color: '#0038A8' },
  { name: 'Engineering', color: '#FFD700' },
  { name: 'Arts & Sciences', color: '#FF4D4D' },
  { name: 'Computer Studies', color: '#1A202C' }
]);

const showModal = ref(false);
const isEditing = ref(false);
const editIndex = ref(null);

const form = reactive({ name: '', color: '#0038A8' });

const openTeamModal = (index = null) => {
  if (index !== null) {
    isEditing.value = true;
    editIndex.value = index;
    form.name = teams.value[index].name;
    form.color = teams.value[index].color;
  } else {
    isEditing.value = false;
    form.name = '';
    form.color = '#0038A8';
  }
  showModal.value = true;
};

const closeModal = () => { showModal.value = false; };

const saveTeam = () => {
  if (!form.name.trim()) return alert("Please enter a team name.");
  if (isEditing.value) teams.value[editIndex.value] = { ...form };
  else teams.value.push({ ...form });
  closeModal();
};

const deleteTeam = (index) => {
  if(confirm(`Are you sure you want to remove ${teams.value[index].name}?`)) {
    teams.value.splice(index, 1);
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
        <span class="value">{{ teams.length }}</span>
      </div>
      <div class="summary-divider"></div>
      <div class="summary-item">
        <span class="label">Active Colleges</span>
        <span class="value">{{ teams.length }}</span>
      </div>
    </div>

    <div class="teams-grid">
      <div v-for="(team, index) in teams" :key="index" class="team-card">
        <div class="card-accent" :style="{ backgroundColor: team.color }"></div>
        <div class="team-card-body">
          <div class="team-icon" :style="{ color: team.color, backgroundColor: team.color + '15' }">
            <i class="fas fa-shield-alt"></i>
          </div>
          <div class="team-info">
            <h3>{{ team.name }}</h3>
            <p>Official Participant</p>
          </div>
        </div>
        <div class="team-card-actions">
          <button class="btn-icon edit" @click="openTeamModal(index)"><i class="fas fa-edit"></i></button>
          <button class="btn-icon delete" @click="deleteTeam(index)"><i class="fas fa-trash-alt"></i></button>
        </div>
      </div>
    </div>
  </div>

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
  transition: transform 0.2s ease;
}

.team-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-md); }

.card-accent { height: 5px; width: 100%; }

.team-card-body {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.team-icon {
  width: 50px; height: 50px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
}

.team-info h3 { margin: 0; font-size: 1.1rem; color: var(--text-main); }
.team-info p { margin: 2px 0 0 0; font-size: 0.85rem; color: var(--text-muted); }

.team-card-actions {
  border-top: 1px solid var(--border-color);
  padding: 12px 20px;
  display: flex; justify-content: flex-end; gap: 10px;
  background: #fafafa;
}

/* Color Picker UI */
.color-picker-row { display: flex; align-items: center; gap: 12px; margin-top: 10px; }
.color-circle-input {
  border: none; width: 48px; height: 48px;
  border-radius: 50%; cursor: pointer; background: none;
}
.color-circle-input::-webkit-color-swatch { border-radius: 50%; border: 2px solid var(--border-color); }

.color-code {
  font-family: monospace; font-weight: 700;
  background: var(--white); padding: 8px 12px;
  border-radius: var(--radius-md); border: 1px solid var(--border-color);
}

.btn-icon { background: none; border: none; cursor: pointer; color: var(--text-muted); padding: 5px; }
.btn-icon:hover { color: var(--adnu-blue-dark); }
.btn-icon.delete:hover { color: var(--adnu-danger); }
</style>