<script setup>
import { ref, reactive } from 'vue';

const teams = ref([
  { name: 'Business & Accountancy', color: '#0038A8' },
  { name: 'Engineering', color: '#FFD700' },
  { name: 'Arts & Sciences', color: '#FF4D4D' },
  { name: 'Computer Studies', color: '#1A202C' }
]);

const showModal = ref(false);
const isEditing = ref(false);
const editIndex = ref(null);

const form = reactive({
  name: '',
  color: '#0038A8'
});

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
  if (isEditing.value) {
    teams.value[editIndex.value] = { ...form };
  } else {
    teams.value.push({ ...form });
  }
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
    <header class="dashboard-header">
  <div class="welcome-text">
    <h1>Teams Management</h1>
    <p>Manage participating colleges and their representative colors.</p>
  </div>
  <div class="header-actions">
    <button class="btn-primary" @click="openTeamModal()">
      <i class="fas fa-plus"></i> Register New Team
    </button>
  </div>
</header>

    <div class="teams-summary">
      <div class="summary-item">
        <span class="label">Total Teams</span>
        <span class="value">{{ teams.length }}</span>
      </div>
      <div class="summary-divider"></div>
      <div class="summary-item">
        <span class="label">Active Colleges</span>
        <span class="value">4</span>
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
          <button class="btn-icon edit" @click="openTeamModal(index)" title="Edit Team">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn-icon delete" @click="deleteTeam(index)" title="Delete Team">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
    </div>

            <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content team-modal">
            <div class="modal-header-section">
            <h3>{{ isEditing ? 'Edit Team Details' : 'Register New Team' }}</h3>
            <p class="modal-subtitle">Configure the identity of the participating college.</p>
            </div>
            
            <div class="modal-form-body">
            <div class="form-group">
                <label>Team/College Name</label>
                <input v-model="form.name" type="text" class="modal-input" placeholder="e.g. Business & Accountancy">
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
            <button class="btn-primary" @click="saveTeam">Confirm Registration</button>
            </div>
        </div>
        </div>
  </div>
</template>

<style scoped>
/* Page Layout */
.page-container {
  padding: 30px;
}

/* Matching the Dashboard Header exactly */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end; /* Aligns buttons to the bottom of the text */
  margin-bottom: 40px;
}

.welcome-text h1 {
  font-size: 2rem;
  color: var(--adnu-blue-navy);
  margin: 0;
}

.welcome-text p {
  color: var(--text-muted);
  margin: 5px 0 0 0;
  font-size: 1rem;
}

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

.summary-item {
  display: flex;
  flex-direction: column;
}

.summary-item .label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  letter-spacing: 1px;
}

.summary-item .value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--adnu-blue-dark);
}

.summary-divider {
  width: 1px;
  height: 30px;
  background: var(--border-color);
  margin: 0 30px;
}

/* Grid Design */
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
  position: relative;
  transition: transform 0.2s ease;
  display: flex;
  flex-direction: column;
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
  align-items: center;
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
}

.team-info h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-main);
}

.team-info p {
  margin: 2px 0 0 0;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.team-card-actions {
  border-top: 1px solid var(--border-color);
  padding: 12px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background: #fafafa;
}

/* Icons Buttons */
.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 5px;
  transition: color 0.2s;
}

.btn-icon.edit { color: var(--text-muted); }
.btn-icon.edit:hover { color: var(--adnu-blue-dark); }
.btn-icon.delete { color: var(--text-muted); }
.btn-icon.delete:hover { color: var(--adnu-danger); }

/* Modal Styling */
.team-modal {
  width: 450px;
  border-top: 5px solid var(--adnu-blue-dark); /* Subtle branding top bar */
}

.modal-header-section h3 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--adnu-blue-navy);
}

.modal-subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 5px 0 25px 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  font-size: 0.8rem;
  color: var(--text-main);
  margin-bottom: 8px;
  text-transform: uppercase;
}

/* Color Picker UI */
.color-picker-row {
  display: flex;
  align-items: center;
  gap: 15px;
}

.color-circle-input {
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  background: none;
}

.color-circle-input::-webkit-color-swatch {
  border-radius: 50%;
  border: 2px solid var(--border-color);
}

.color-code {
  font-family: monospace;
  font-weight: 700;
  color: var(--text-muted);
}
</style>