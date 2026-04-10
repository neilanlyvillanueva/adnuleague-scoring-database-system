<script setup>
import { ref, reactive } from 'vue';

const dynamicData = reactive({
  userName: 'Admin User'
});

const currentDate = ref(new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }));

const standings = ref([
  { name: 'Business & Accountancy', gold: 5, silver: 3, bronze: 2, points: 120, color: '#0038A8' },
  { name: 'Engineering', gold: 4, silver: 5, bronze: 1, points: 115, color: '#FFD700' },
  { name: 'Arts & Sciences', gold: 3, silver: 2, bronze: 6, points: 95, color: '#FF4D4D' },
  { name: 'Computer Studies', gold: 2, silver: 4, bronze: 3, points: 88, color: '#1A202C' },
]);

// Modal Logic
const isModalOpen = ref(false);
const currentEditingKey = ref('');
const tempEditValue = ref('');

const openEditModal = (key) => {
  currentEditingKey.value = key;
  tempEditValue.value = dynamicData[key];
  isModalOpen.value = true;
};

const closeModal = () => isModalOpen.value = false;

const saveEdit = () => {
  if (tempEditValue.value.trim() !== '') {
    dynamicData[currentEditingKey.value] = tempEditValue.value;
  }
  closeModal();
};
</script>

<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="welcome-text">
        <h1>Dashboard</h1>
        <p>Welcome back, <span @click="openEditModal('userName')" class="editable-text">{{ dynamicData.userName }} <i class="fa-solid fa-pen"></i></span></p>
      </div>
      <div class="date-display">
        {{ currentDate }}
      </div>
    </header>

    <section class="stats-grid">
  <div class="stat-card clickable" @click="$router.push('/teams')">
    <div class="stat-icon blue"><i class="fas fa-users"></i></div>
    <div class="stat-info">
      <h3>Teams</h3>
      <p class="stat-number">12</p>
    </div>
  </div>

  <div class="stat-card clickable" @click="$router.push('/events')">
    <div class="stat-icon gold"><i class="fas fa-trophy"></i></div>
    <div class="stat-info">
      <h3>Total Events</h3>
      <p class="stat-number">24</p>
    </div>
  </div>
  
  <div class="stat-card clickable" @click="$router.push('/scoring')">
    <div class="stat-icon navy"><i class="fas fa-check-double"></i></div>
    <div class="stat-info">
      <h3>Completion</h3>
      <p class="stat-number">65%</p>
    </div>
  </div>

  <div class="stat-card clickable" @click="$router.push('/matches')">
    <div class="stat-icon red"><i class="fas fa-broadcast-tower"></i></div>
    <div class="stat-info">
      <h3>Live Matches</h3>
      <p class="stat-number">3</p>
    </div>
  </div>
</section>

    <div class="dashboard-content">
      <div class="content-card standings">
        <div class="card-header">
          <h2>Overall Leaderboard</h2>
          <button class="btn-primary">View Full Standings</button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Team Name</th>
              <th>Gold</th>
              <th>Silver</th>
              <th>Bronze</th>
              <th>Total Points</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(team, index) in standings" :key="team.name">
              <td><strong>#{{ index + 1 }}</strong></td>
              <td class="team-cell">
                <div class="team-color" :style="{ backgroundColor: team.color }"></div>
                {{ team.name }}
              </td>
              <td>{{ team.gold }}</td>
              <td>{{ team.silver }}</td>
              <td>{{ team.bronze }}</td>
              <td class="points-cell">{{ team.points }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>Edit {{ currentEditingKey === 'userName' ? 'User Name' : 'Field' }}</h3>
        <input v-model="tempEditValue" type="text" class="modal-input" @keyup.enter="saveEdit" />
        <div class="modal-actions">
          <button class="btn-ghost" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveEdit">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 30px;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
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
}

.editable-text {
  color: var(--adnu-blue-dark);
  cursor: pointer;
  font-weight: 600;
}

.editable-text i {
  font-size: 0.8rem;
  margin-left: 5px;
  opacity: 0.6;
}

.date-display {
  color: var(--text-muted);
  font-weight: 500;
}

/* Stats Cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: var(--white);
  padding: 20px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-card.clickable {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card.clickable:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--adnu-gold);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-icon.blue { 
    background: var(--adnu-blue-light); 
    color: var(--adnu-blue-dark); 
}

.stat-icon.gold { 
    background: #FFF9E6; 
    color: var(--adnu-gold); 
}

.stat-icon.red { 
    background: #FFEBEB; 
    color: var(--adnu-live-red); 
}

.stat-icon.navy { 
    background: #E2E8F0; 
    color: var(--adnu-blue-navy); 
}

.stat-info h3 {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  margin: 5px 0 0 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
}

/* Standings Table */
.content-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h2 {
  font-size: 1.25rem;
  color: var(--adnu-blue-navy);
  margin: 0;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 12px;
  border-bottom: 2px solid var(--border-color);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.data-table td {
  padding: 15px 12px;
  border-bottom: 1px solid var(--border-color);
}

.team-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.team-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.points-cell {
  font-weight: 700;
  color: var(--adnu-blue-dark);
}

.progress-bar-mini {
  width: 100%;
  height: 4px;
  background: var(--border-color);
  border-radius: 2px;
  margin-top: 8px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--adnu-blue-dark);
  border-radius: 2px;
}

.stat-icon.navy { 
  background: #E8F0FF; 
  color: var(--adnu-blue-navy); 
}

/* Modal Styling from Global Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 31, 92, 0.7); /* adnu-blue-navy with opacity */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--white);
  color: var(--text-main);
  padding: 24px;
  border-radius: var(--radius-lg);
  width: 300px;
  box-shadow: var(--shadow-md);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.1rem;
  color: var(--adnu-blue-dark);
}

.modal-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 1rem;
  box-sizing: border-box;
  font-family: var(--font-main);
  color: var(--text-main);
}

.modal-input:focus {
  outline: none;
  border-color: var(--adnu-blue-dark);
  box-shadow: 0 0 0 2px var(--adnu-blue-light);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-save { 
    background: var(--adnu-blue-light); 
    color: var(--adnu-blue-dark); 
    border: none; 
    padding: 8px 16px; 
    border-radius: 4px; 
    cursor: pointer; 
}

.btn-cancel { 
    background: var(--adnu-danger); 
    color: var(--adnu-live-red);
    border: 1px solid var(--adnu-danger);
    padding: 8px 16px; 
    border-radius: 4px; 
    cursor: pointer; 
}

.btn-save:hover { 
    color: var(--adnu-blue-light); 
    background: var(--adnu-blue-dark);
}

.btn-cancel:hover { 
    background: var(--adnu-danger-strong); 
    color: var(--white);
}
</style>