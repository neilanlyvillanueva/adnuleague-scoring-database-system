<script setup>
import { reactive, watch } from 'vue';

const props = defineProps({
  show: Boolean,
  match: Object,
  event: Object,
  teams: Array
});

const emit = defineEmits(['close', 'finalize']);

const form = reactive({
  scores: {},
  setScores: []
});

const getTeamName = (id) => props.teams.find(t => t.id === id)?.name || 'Unknown';

watch(() => props.match, (newMatch) => {
  if (newMatch && props.event) {
    form.scores = {};
    form.setScores = [];

    if (newMatch.matchupType === '1v1') {
      form.scores.teamA = 0;
      form.scores.teamB = 0;
    } else {
      newMatch.participants?.forEach(p => {
        form.scores[p] = 0;
      });
    }

    // Initialize set scores if threshold incremental
    if (props.event?.thresholdIncremental && props.event.sets) {
      for (let i = 0; i < props.event.sets; i++) {
        if (newMatch.matchupType === '1v1') {
          form.setScores.push({ set: i + 1, teamA: 0, teamB: 0 });
        } else {
          const setScore = { set: i + 1 };
          newMatch.participants?.forEach(p => {
            setScore[p] = 0;
          });
          form.setScores.push(setScore);
        }
      }
    }
  }
}, { immediate: true });

const handleFinalize = () => {
  emit('finalize', { ...form });
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content finalize-modal">
      <div class="modal-header-section">
        <h3>Finalize Match</h3>
        <p class="modal-subtitle">
          {{ event?.name }} - {{ match?.venue }}
        </p>
      </div>

      <div class="modal-form-body">
        <!-- Set Scores (Threshold Incremental) -->
        <div v-if="event?.thresholdIncremental && form.setScores.length > 0" class="set-scores-section">
          <h4>Set Scores</h4>

          <!-- 1v1 Set Scores -->
          <div v-if="match?.matchupType === '1v1'">
            <div v-for="(set, index) in form.setScores" :key="index" class="set-row">
              <span class="set-label">Set {{ set.set }}</span>
              <div class="set-inputs">
                <div class="team-input">
                  <span class="team-label">{{ getTeamName(match.teamAId) }}</span>
                  <input type="number" v-model.number="set.teamA" class="score-input" min="0">
                </div>
                <span class="set-separator">-</span>
                <div class="team-input">
                  <span class="team-label">{{ getTeamName(match.teamBId) }}</span>
                  <input type="number" v-model.number="set.teamB" class="score-input" min="0">
                </div>
              </div>
            </div>
            <div class="set-summary">
              <strong>Sets Won:</strong>
              <span>{{ getTeamName(match.teamAId) }}: {{ form.setScores.filter(s => s.teamA > s.teamB).length }}</span>
              <span>{{ getTeamName(match.teamBId) }}: {{ form.setScores.filter(s => s.teamB > s.teamA).length }}</span>
            </div>
          </div>

          <!-- FFA Set Scores -->
          <div v-else>
            <div v-for="(set, index) in form.setScores" :key="index" class="set-row ffa-set">
              <span class="set-label">Set {{ set.set }}</span>
              <div class="ffa-set-inputs">
                <div v-for="participantId in match?.participants" :key="participantId" class="team-input">
                  <span class="team-label">{{ getTeamName(participantId) }}</span>
                  <input type="number" v-model.number="set[participantId]" class="score-input" min="0">
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Regular Scores (non-set based) -->
        <div v-else class="regular-scores-section">
          <h4>Final Scores</h4>

          <div v-if="match?.matchupType === '1v1'" class="score-row">
            <div class="team-input">
              <span class="team-label">{{ getTeamName(match.teamAId) }}</span>
              <input type="number" v-model.number="form.scores.teamA" class="score-input" min="0">
            </div>
            <span class="score-separator">-</span>
            <div class="team-input">
              <span class="team-label">{{ getTeamName(match.teamBId) }}</span>
              <input type="number" v-model.number="form.scores.teamB" class="score-input" min="0">
            </div>
          </div>

          <div v-else class="ffa-scores">
            <div v-for="participantId in match?.participants" :key="participantId" class="score-row">
              <span class="team-label">{{ getTeamName(participantId) }}</span>
              <input type="number" v-model.number="form.scores[participantId]" class="score-input" min="0">
            </div>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn-ghost" @click="emit('close')">Cancel</button>
        <button class="btn-primary" @click="handleFinalize">
          <i class="fas fa-check"></i> Confirm Results
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border-top: 6px solid var(--adnu-gold);
}

.modal-header-section {
  padding: 24px 24px 16px 24px;
}

.modal-header-section h3 {
  margin: 0 0 4px 0;
  font-size: 1.4rem;
  color: var(--adnu-blue-navy);
  font-weight: 700;
}

.modal-subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 0;
}

.modal-form-body {
  padding: 0 24px 24px 24px;
}

.set-scores-section h4,
.regular-scores-section h4 {
  font-size: 0.9rem;
  color: var(--adnu-blue-navy);
  margin: 0 0 15px 0;
  font-weight: 700;
}

.set-row {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  background: var(--bg-gray-light);
  border-radius: var(--radius-md);
  margin-bottom: 10px;
}

.set-label {
  font-weight: 700;
  font-size: 0.85rem;
  color: var(--adnu-blue-navy);
  min-width: 60px;
}

.set-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.team-input {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.team-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
}

.score-input {
  padding: 8px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

.score-input:focus {
  outline: none;
  border-color: var(--adnu-blue-dark);
}

.set-separator,
.score-separator {
  font-weight: 700;
  color: var(--text-muted);
  font-size: 1.2rem;
}

.set-summary {
  display: flex;
  gap: 20px;
  padding: 12px;
  background: var(--adnu-blue-light);
  border-radius: var(--radius-md);
  margin-top: 10px;
}

.set-summary strong {
  color: var(--adnu-blue-navy);
}

.ffa-set {
  flex-direction: column;
  gap: 10px;
}

.ffa-set-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
  width: 100%;
}

.score-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.score-row .team-label {
  min-width: 150px;
}

.ffa-scores .score-row {
  justify-content: space-between;
}

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
