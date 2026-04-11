<script setup>
defineProps({
  match: {
    type: Object,
    required: true
  },
  event: {
    type: Object,
    required: true
  },
  teams: {
    type: Array,
    required: true
  }
});

const getTeamName = (id) => teams.find(t => t.id === id)?.name || 'Unknown';
const getTeamColor = (id) => teams.find(t => t.id === id)?.color || '#ccc';
</script>

<template>
  <div class="live-match-card">
    <div class="live-match-header">
      <span class="event-tag">{{ event?.name || 'Unknown Event' }}</span>
      <span class="venue-tag"><i class="fas fa-map-marker-alt"></i> {{ match.venue }}</span>
    </div>

    <div class="live-match-content">
      <!-- 1v1 Matchup -->
      <div v-if="match.matchupType === '1v1'" class="matchup-1v1">
        <div class="team-side">
          <span class="team-name" :style="{ color: getTeamColor(match.teamAId) }">
            {{ getTeamName(match.teamAId) }}
          </span>
          <span class="team-score">{{ match.scores?.teamA || 0 }}</span>
        </div>
        <div class="vs-divider">VS</div>
        <div class="team-side">
          <span class="team-name" :style="{ color: getTeamColor(match.teamBId) }">
            {{ getTeamName(match.teamBId) }}
          </span>
          <span class="team-score">{{ match.scores?.teamB || 0 }}</span>
        </div>
      </div>

      <!-- Free-for-All Matchup -->
      <div v-else class="matchup-ffa">
        <div v-for="participantId in match.participants" :key="participantId" class="ffa-participant">
          <span class="team-name" :style="{ color: getTeamColor(participantId) }">
            {{ getTeamName(participantId) }}
          </span>
          <span class="team-score">{{ match.scores?.[participantId] || 0 }}</span>
        </div>
      </div>
    </div>

    <div class="live-match-footer">
      <span class="live-badge">
        <i class="fas fa-circle"></i> LIVE
      </span>
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<style scoped>
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
</style>
