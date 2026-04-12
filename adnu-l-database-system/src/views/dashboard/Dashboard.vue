<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from '../../composables/useStore';
import { useAuth } from '../../composables/useAuth';

const { state, getLeaderboard, fetchMatches, fetchLeaderboard } = useStore();
const { userRole } = useAuth();

const getUserNameKey = () => {
  const role = userRole.value || 'admin';
  return `adnl_user_name_${role}`;
};

const dynamicData = reactive({
  userName: 'Admin User'
});

// Load the username for current role on mount
const loadUserName = () => {
  const role = userRole.value || 'admin';
  const defaultName = role === 'tabulation' ? 'Tabulation User' : 'Admin User';
  dynamicData.userName = localStorage.getItem(`adnl_user_name_${role}`) || defaultName;
};

const currentDate = ref(new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }));

// Fetch data on mount
onMounted(async () => {
  loadUserName();
  await Promise.all([fetchMatches(), fetchLeaderboard()]);
});

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
    if (currentEditingKey.value === 'userName') {
      const role = userRole.value || 'admin';
      localStorage.setItem(`adnl_user_name_${role}`, tempEditValue.value);
    }
  }
  closeModal();
};

// Computed stats
const totalTeams = computed(() => state.teams.length);
const totalEvents = computed(() => state.events.length);
const ongoingMatches = computed(() => state.matches.filter(m => m.status === 'ongoing'));
const completedMatches = computed(() => state.matches.filter(m => m.status === 'completed'));

const completionRate = computed(() => {
  const total = ongoingMatches.value.length + completedMatches.value.length;
  if (total === 0) return 0;
  return Math.round((completedMatches.value.length / total) * 100);
});

const leaderboard = computed(() => getLeaderboard().slice(0, 5));

const getTeam = (teamId) => state.teams.find(t => t.id === teamId);
const getEvent = (eventId) => state.events.find(e => e.id === eventId);
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
          <p class="stat-number">{{ totalTeams }}</p>
        </div>
      </div>

      <div class="stat-card clickable" @click="$router.push('/events')">
        <div class="stat-icon gold"><i class="fas fa-trophy"></i></div>
        <div class="stat-info">
          <h3>Total Events</h3>
          <p class="stat-number">{{ totalEvents }}</p>
        </div>
      </div>

      <div class="stat-card clickable" @click="$router.push('/matches')">
        <div class="stat-icon navy"><i class="fas fa-check-double"></i></div>
        <div class="stat-info">
          <h3>Completion</h3>
          <p class="stat-number">{{ completionRate }}%</p>
          <div class="progress-bar-mini">
            <div class="progress-fill" :style="{ width: completionRate + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="stat-card clickable" @click="$router.push('/matches')">
        <div class="stat-icon red"><i class="fas fa-broadcast-tower"></i></div>
        <div class="stat-info">
          <h3>Live Matches</h3>
          <p class="stat-number">{{ ongoingMatches.length }}</p>
        </div>
      </div>
    </section>

    <!-- Live Matches Section -->
    <div v-if="ongoingMatches.length > 0" class="live-matches-section">
      <div class="content-card">
        <div class="card-header">
          <h2><i class="fas fa-circle live-dot"></i> Live Matches</h2>
          <button class="btn-primary btn-sm" @click="$router.push('/matches')">View All</button>
        </div>
        <div class="live-matches-grid">
          <div v-for="match in ongoingMatches" :key="match.id" class="live-match-card">
            <div class="live-match-header">
              <span class="event-tag">{{ getEvent(match.eventId)?.name || 'Unknown Event' }}</span>
              <span class="venue-tag"><i class="fas fa-map-marker-alt"></i> {{ match.venue }}</span>
            </div>

            <div class="live-match-content">
              <div v-if="match.matchupType === '1v1'" class="matchup-1v1">
                <div class="team-side">
                  <span class="team-name" :style="{ color: getTeam(match.teamAId)?.color }">
                    {{ getTeam(match.teamAId)?.name || 'Team A' }}
                  </span>
                  <span class="team-score">{{ match.scores?.teamA || 0 }}</span>
                </div>
                <div class="vs-divider">VS</div>
                <div class="team-side">
                  <span class="team-name" :style="{ color: getTeam(match.teamBId)?.color }">
                    {{ getTeam(match.teamBId)?.name || 'Team B' }}
                  </span>
                  <span class="team-score">{{ match.scores?.teamB || 0 }}</span>
                </div>
              </div>

              <div v-else class="matchup-ffa">
                <div v-for="participantId in match.participants" :key="participantId" class="ffa-participant">
                  <span class="team-name" :style="{ color: getTeam(participantId)?.color }">
                    {{ getTeam(participantId)?.name || 'Unknown' }}
                  </span>
                  <span class="team-score">{{ match.scores?.[participantId] || 0 }}</span>
                </div>
              </div>
            </div>

            <div class="live-match-footer">
              <span class="live-badge">
                <i class="fas fa-circle"></i> LIVE
              </span>
              <button class="btn-sm btn-ghost" @click="$router.push('/matches')">
                <i class="fas fa-external-link-alt"></i> Manage
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Overall Standings -->
    <div class="dashboard-content">
      <div class="content-card standings">
        <div class="card-header">
          <h2>Overall Leaderboard</h2>
          <button class="btn-primary btn-sm" @click="$router.push('/leaderboard')">View Full Standings</button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Team Name</th>
              <th>Total Wins</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, index) in leaderboard" :key="entry.teamId">
              <td><strong>#{{ index + 1 }}</strong></td>
              <td class="team-cell">
                <div class="team-color" :style="{ backgroundColor: getTeam(entry.teamId)?.color }"></div>
                {{ entry.teamName }}
              </td>
              <td class="wins-cell">{{ entry.wins }}</td>
            </tr>
            <tr v-if="leaderboard.length === 0">
              <td colspan="3" class="no-data">
                <i class="fas fa-trophy"></i>
                <p>No matches completed yet</p>
              </td>
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

.stat-icon.blue { background: var(--adnu-blue-light); color: var(--adnu-blue-dark); }
.stat-icon.gold { background: #FFF9E6; color: var(--adnu-gold); }
.stat-icon.red { background: #FFEBEB; color: var(--adnu-live-red); }
.stat-icon.navy { background: var(--adnu-blue-light); color: var(--adnu-blue-navy); }

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
  transition: width 0.3s ease;
}

/* Live Matches Section */
.live-matches-section {
  margin-bottom: 40px;
}

.live-matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.live-match-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.live-match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-gray-light);
  border-bottom: 1px solid var(--border-color);
}

.event-tag {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
  padding: 4px 10px;
  border-radius: 4px;
}

.venue-tag {
  font-size: 0.75rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 5px;
}

.venue-tag i {
  font-size: 0.7rem;
}

.live-match-content {
  padding: 20px;
}

.matchup-1v1 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.team-side {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.team-name {
  font-weight: 600;
  font-size: 0.95rem;
  text-align: center;
}

.team-score {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--adnu-blue-navy);
}

.vs-divider {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted);
  padding: 0 16px;
}

.matchup-ffa {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ffa-participant {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--bg-gray-light);
  border-radius: var(--radius-md);
}

.live-match-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-top: 1px solid var(--border-color);
  background: #fafafa;
}

.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--adnu-live-red);
}

.live-badge i {
  font-size: 0.5rem;
}

.btn-sm {
  padding: 8px 14px;
  font-size: 0.85rem;
  border-radius: var(--radius-md);
}

.btn-sm.btn-ghost {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-sm.btn-ghost:hover {
  background: var(--adnu-blue-light);
  color: var(--adnu-blue-dark);
  border-color: var(--adnu-blue-dark);
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
  display: flex;
  align-items: center;
  gap: 10px;
}

.live-dot {
  color: var(--adnu-live-red);
  font-size: 0.8rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
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

.wins-cell {
  font-weight: 700;
  color: var(--adnu-blue-dark);
}

.no-data {
  text-align: center;
  padding: 40px 20px !important;
  color: var(--text-muted);
}

.no-data i {
  font-size: 2rem;
  display: block;
  margin-bottom: 10px;
  color: var(--adnu-gold);
  opacity: 0.5;
}

.no-data p {
  margin: 0;
  font-size: 0.95rem;
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 31, 92, 0.7);
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
</style>
