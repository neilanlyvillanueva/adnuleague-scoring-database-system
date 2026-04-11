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

defineEmits(['finalize', 'delete']);

const getTeamName = (id) => teams.find(t => t.id === id)?.name || 'Unknown';
const getTeamColor = (id) => teams.find(t => t.id === id)?.color || '#ccc';
</script>

<template>
  <div :class="['match-card', match.status]">
    <div class="match-header">
      <span class="event-badge">{{ event?.name || 'Unknown Event' }}</span>
      <span class="venue-badge">
        <i class="fas fa-map-marker-alt"></i> {{ match.venue }}
      </span>
    </div>

    <div class="match-content">
      <!-- 1v1 Matchup -->
      <div v-if="match.matchupType === '1v1'" class="matchup-1v1">
        <div class="team-side" :class="{ winner: match.status === 'completed' && match.winner === match.teamAId }">
          <span class="team-name" :style="{ color: getTeamColor(match.teamAId) }">
            {{ getTeamName(match.teamAId) }}
            <i v-if="match.status === 'completed' && match.winner === match.teamAId" class="fas fa-trophy winner-icon"></i>
          </span>
          <span class="team-score">{{ match.scores?.teamA || 0 }}</span>
        </div>
        <div class="vs-divider">VS</div>
        <div class="team-side" :class="{ winner: match.status === 'completed' && match.winner === match.teamBId }">
          <span class="team-name" :style="{ color: getTeamColor(match.teamBId) }">
            {{ getTeamName(match.teamBId) }}
            <i v-if="match.status === 'completed' && match.winner === match.teamBId" class="fas fa-trophy winner-icon"></i>
          </span>
          <span class="team-score">{{ match.scores?.teamB || 0 }}</span>
        </div>
      </div>

      <!-- Free-for-All Matchup -->
      <div v-else class="matchup-ffa">
        <div
          v-for="participantId in match.participants"
          :key="participantId"
          :class="['ffa-participant', { winner: match.status === 'completed' && match.winner === participantId }]"
        >
          <span class="team-name" :style="{ color: getTeamColor(participantId) }">
            {{ getTeamName(participantId) }}
            <i v-if="match.status === 'completed' && match.winner === participantId" class="fas fa-trophy winner-icon"></i>
          </span>
          <span class="team-score">{{ match.scores?.[participantId] || 0 }}</span>
        </div>
      </div>
    </div>

    <div v-if="match.status === 'ongoing'" class="match-actions">
      <button class="btn-sm btn-primary" @click="$emit('finalize', match)">
        <i class="fas fa-check"></i> Finalize
      </button>
      <button class="btn-sm btn-ghost" @click="$emit('delete', match.id)">
        <i class="fas fa-trash"></i>
      </button>
    </div>
  </div>
</template>

<style scoped>
.match-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.match-card.ongoing {
  border-left: 4px solid var(--adnu-live-red);
}

.match-card.completed {
  border-left: 4px solid var(--adnu-gold);
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-gray-light);
  border-bottom: 1px solid var(--border-color);
}

.event-badge {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
  padding: 4px 10px;
  border-radius: 4px;
}

.venue-badge {
  font-size: 0.75rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 5px;
}

.venue-badge i {
  font-size: 0.7rem;
}

.match-content {
  padding: 20px;
}

/* 1v1 Matchup */
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
  padding: 12px;
  border-radius: var(--radius-md);
  transition: background 0.2s;
}

.team-side.winner {
  background: #FFF9E6;
}

.team-name {
  font-weight: 600;
  font-size: 0.95rem;
  text-align: center;
}

.winner-icon {
  color: var(--adnu-gold);
  margin-left: 6px;
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

/* FFA Matchup */
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

.ffa-participant.winner {
  background: #FFF9E6;
  border: 1px solid var(--adnu-gold);
}

.ffa-participant .team-name {
  display: flex;
  align-items: center;
  gap: 6px;
}

.match-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 12px 16px;
  border-top: 1px solid var(--border-color);
  background: #fafafa;
}

.btn-sm {
  padding: 8px 14px;
  font-size: 0.85rem;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-sm.btn-primary {
  background: var(--adnu-blue-dark);
  color: var(--white);
}

.btn-sm.btn-primary:hover {
  background: var(--adnu-blue-navy);
}

.btn-sm.btn-ghost {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.btn-sm.btn-ghost:hover {
  background: var(--adnu-danger-light);
  color: var(--adnu-danger);
  border-color: var(--adnu-danger);
}
</style>
