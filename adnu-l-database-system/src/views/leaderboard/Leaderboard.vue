<script setup>
import { computed } from 'vue';
import { useStore } from '../../composables/useStore';

const { state, getLeaderboard } = useStore();

const leaderboard = computed(() => getLeaderboard());

const getTeam = (teamId) => state.teams.find(t => t.id === teamId);

// Calculate podium positions
const podiumTeams = computed(() => leaderboard.value.slice(0, 3));
const remainingTeams = computed(() => leaderboard.value.slice(3));

// Get rank icon/medal
const getMedal = (rank) => {
  if (rank === 1) return { icon: 'fas fa-medal', color: '#FFD700', label: 'Gold' };
  if (rank === 2) return { icon: 'fas fa-medal', color: '#C0C0C0', label: 'Silver' };
  if (rank === 3) return { icon: 'fas fa-medal', color: '#CD7F32', label: 'Bronze' };
  return null;
};
</script>

<template>
  <div class="page-container">
    <header class="dashboard-header">
      <div class="welcome-text">
        <h1>Overall Leaderboard</h1>
        <p>Team rankings based on total match wins across all events.</p>
      </div>
    </header>

    <!-- Podium Display -->
    <div v-if="podiumTeams.length > 0" class="podium-section">
      <div class="podium">
        <!-- 2nd Place -->
        <div v-if="podiumTeams[1]" class="podium-team second">
          <div class="medal-icon">
            <i class="fas fa-medal"></i>
          </div>
          <div class="team-info">
            <div class="team-color-dot" :style="{ backgroundColor: getTeam(podiumTeams[1].teamId)?.color }"></div>
            <span class="team-name">{{ podiumTeams[1].teamName }}</span>
          </div>
          <div class="wins-display">
            <span class="wins-count">{{ podiumTeams[1].wins }}</span>
            <span class="wins-label">Wins</span>
          </div>
          <div class="rank-badge">2</div>
        </div>

        <!-- 1st Place (Center, Elevated) -->
        <div v-if="podiumTeams[0]" class="podium-team first">
          <div class="medal-icon">
            <i class="fas fa-medal"></i>
          </div>
          <div class="team-info">
            <div class="team-color-dot" :style="{ backgroundColor: getTeam(podiumTeams[0].teamId)?.color }"></div>
            <span class="team-name">{{ podiumTeams[0].teamName }}</span>
          </div>
          <div class="wins-display">
            <span class="wins-count">{{ podiumTeams[0].wins }}</span>
            <span class="wins-label">Wins</span>
          </div>
          <div class="rank-badge">1</div>
        </div>

        <!-- 3rd Place -->
        <div v-if="podiumTeams[2]" class="podium-team third">
          <div class="medal-icon">
            <i class="fas fa-medal"></i>
          </div>
          <div class="team-info">
            <div class="team-color-dot" :style="{ backgroundColor: getTeam(podiumTeams[2].teamId)?.color }"></div>
            <span class="team-name">{{ podiumTeams[2].teamName }}</span>
          </div>
          <div class="wins-display">
            <span class="wins-count">{{ podiumTeams[2].wins }}</span>
            <span class="wins-label">Wins</span>
          </div>
          <div class="rank-badge">3</div>
        </div>
      </div>
    </div>

    <!-- Full Leaderboard Table -->
    <div class="leaderboard-table-section">
      <div class="table-card">
        <table class="leaderboard-table">
          <thead>
            <tr>
              <th class="rank-col">Rank</th>
              <th>Team</th>
              <th class="wins-col">Total Wins</th>
              <th class="trend-col">Trend</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, index) in leaderboard" :key="entry.teamId" class="leaderboard-row">
              <td class="rank-cell">
                <span class="rank-number" :class="getMedal(index + 1) ? 'medal-rank' : ''">
                  {{ index + 1 }}
                </span>
              </td>
              <td class="team-cell">
                <div class="team-info-cell">
                  <div class="team-color-bar" :style="{ backgroundColor: getTeam(entry.teamId)?.color }"></div>
                  <span class="team-name">{{ entry.teamName }}</span>
                </div>
              </td>
              <td class="wins-cell">
                <span class="wins-badge">{{ entry.wins }}</span>
              </td>
              <td class="trend-cell">
                <span v-if="index === 0" class="trend-indicator up">
                  <i class="fas fa-arrow-up"></i> Leading
                </span>
                <span v-else-if="entry.wins === leaderboard[0]?.wins" class="trend-indicator tied">
                  <i class="fas fa-equals"></i> Tied
                </span>
                <span v-else class="trend-indicator">
                  <i class="fas fa-minus"></i> {{ leaderboard[0]?.wins - entry.wins }} behind
                </span>
              </td>
            </tr>
            <tr v-if="leaderboard.length === 0" class="no-data-row">
              <td colspan="4">
                <i class="fas fa-trophy"></i>
                <p>No matches completed yet. Start finalizing matches to see rankings.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  padding: 30px;
}

.dashboard-header {
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

/* Podium Section */
.podium-section {
  margin-bottom: 50px;
}

.podium {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 20px;
  padding: 40px 20px;
  background: linear-gradient(180deg, var(--bg-gray-light) 0%, var(--white) 100%);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.podium-team {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-radius: var(--radius-lg);
  background: var(--white);
  box-shadow: var(--shadow-md);
  position: relative;
  min-width: 180px;
  transition: transform 0.2s;
}

.podium-team:hover {
  transform: translateY(-5px);
}

.podium-team.first {
  order: 2;
  background: linear-gradient(135deg, #FFF9E6 0%, var(--white) 100%);
  border: 2px solid var(--adnu-gold);
  transform: scale(1.05);
}

.podium-team.first:hover {
  transform: scale(1.05) translateY(-5px);
}

.podium-team.second {
  order: 1;
  background: linear-gradient(135deg, #E8E8E8 0%, var(--white) 100%);
  border: 2px solid #C0C0C0;
}

.podium-team.third {
  order: 3;
  background: linear-gradient(135deg, #FFE4C4 0%, var(--white) 100%);
  border: 2px solid #CD7F32;
}

.medal-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.podium-team.first .medal-icon {
  color: var(--adnu-gold);
}

.podium-team.second .medal-icon {
  color: #C0C0C0;
}

.podium-team.third .medal-icon {
  color: #CD7F32;
}

.team-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
}

.team-color-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid var(--border-color);
}

.team-name {
  font-weight: 700;
  font-size: 1rem;
  color: var(--adnu-blue-navy);
  text-align: center;
}

.wins-display {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.wins-count {
  font-size: 2rem;
  font-weight: 700;
  color: var(--adnu-blue-dark);
}

.wins-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
}

.rank-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--adnu-blue-dark);
  color: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: var(--shadow-md);
}

/* Leaderboard Table */
.leaderboard-table-section {
  max-width: 900px;
  margin: 0 auto;
}

.table-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
}

.leaderboard-table th {
  text-align: left;
  padding: 16px;
  border-bottom: 2px solid var(--border-color);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rank-col {
  width: 80px;
  text-align: center;
}

.wins-col {
  width: 120px;
}

.trend-col {
  width: 150px;
}

.leaderboard-row {
  transition: background 0.2s;
}

.leaderboard-row:hover {
  background: var(--bg-gray-light);
}

.leaderboard-row td {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
}

.rank-cell {
  text-align: center;
}

.rank-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-gray-light);
  font-weight: 700;
  color: var(--text-muted);
}

.rank-number.medal-rank {
  background: transparent;
  font-size: 1.2rem;
}

.team-cell {
  padding: 16px !important;
}

.team-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.team-color-bar {
  width: 4px;
  height: 30px;
  border-radius: 2px;
  flex-shrink: 0;
}

.team-name {
  font-weight: 600;
  color: var(--text-main);
  font-size: 0.95rem;
}

.wins-cell {
  text-align: center;
}

.wins-badge {
  display: inline-block;
  padding: 6px 14px;
  background: var(--adnu-blue-light);
  color: var(--adnu-blue-dark);
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
}

.trend-cell {
  font-size: 0.85rem;
}

.trend-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-muted);
}

.trend-indicator.up {
  color: #2E7D32;
}

.trend-indicator.tied {
  color: var(--adnu-gold);
}

.no-data-row td {
  text-align: center;
  padding: 60px 20px !important;
  color: var(--text-muted);
}

.no-data-row i {
  font-size: 3rem;
  display: block;
  margin-bottom: 12px;
  color: var(--adnu-gold);
  opacity: 0.5;
}

.no-data-row p {
  margin: 0;
  font-size: 0.95rem;
}
</style>
