<script setup>
defineProps({
  leaderboard: {
    type: Array,
    required: true
  },
  teams: {
    type: Array,
    required: true
  }
});

const getTeam = (teamId) => teams.find(t => t.id === teamId);

const getMedal = (rank) => {
  if (rank === 1) return { icon: 'fas fa-medal', color: '#FFD700', label: 'Gold' };
  if (rank === 2) return { icon: 'fas fa-medal', color: '#C0C0C0', label: 'Silver' };
  if (rank === 3) return { icon: 'fas fa-medal', color: '#CD7F32', label: 'Bronze' };
  return null;
};
</script>

<template>
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
</template>

<style scoped>
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
