<script setup>
import { computed } from 'vue';

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

const podiumTeams = computed(() => leaderboard.slice(0, 3));
</script>

<template>
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
</template>

<style scoped>
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
</style>
