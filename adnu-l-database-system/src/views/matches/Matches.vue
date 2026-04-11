<script setup>
import { ref, computed } from 'vue';
import { useStore } from '../../composables/useStore';
import MatchModal from '../../components/modals/MatchModal.vue';
import FinalizeMatchModal from '../../components/modals/FinalizeMatchModal.vue';
import MatchCard from '../../components/cards/MatchCard.vue';

const { state, addMatch, updateMatch, finalizeMatch, deleteMatch, updateTeamWins } = useStore();

const showModal = ref(false);
const showFinalizeModal = ref(false);
const editingMatch = ref(null);
const selectedMatch = ref(null);

const ongoingMatches = computed(() => state.matches.filter(m => m.status === 'ongoing'));
const completedMatches = computed(() => state.matches.filter(m => m.status === 'completed'));

const getEvent = (eventId) => state.events.find(e => e.id === eventId);

const openMatchModal = (match = null) => {
  editingMatch.value = match;
  showModal.value = true;
};

const openFinalizeModal = (match) => {
  selectedMatch.value = match;
  showFinalizeModal.value = true;
};

const closeModals = () => {
  showModal.value = false;
  showFinalizeModal.value = false;
  editingMatch.value = null;
  selectedMatch.value = null;
};

const handleSaveMatch = (matchData) => {
  // Validation
  if (!matchData.eventId) {
    alert('Please select an event/sport');
    return;
  }
  if (!matchData.venue.trim()) {
    alert('Please enter a venue');
    return;
  }

  const participatingTeams = state.teams.filter(t => t.participatingSports?.includes(matchData.eventId));

  if (matchData.matchupType === '1v1') {
    if (!matchData.teamAId || !matchData.teamBId) {
      alert('Please select both teams');
      return;
    }
    if (matchData.teamAId === matchData.teamBId) {
      alert('Teams must be different');
      return;
    }
  } else {
    if (matchData.participants.length < 2) {
      alert('Please select at least 2 participants for Free-for-All');
      return;
    }
  }

  const newMatchData = {
    eventId: matchData.eventId,
    matchupType: matchData.matchupType,
    teamAId: matchData.teamAId,
    teamBId: matchData.teamBId,
    participants: matchData.participants,
    venue: matchData.venue,
    scores: matchData.matchupType === '1v1' ? { teamA: 0, teamB: 0 } : {},
    status: 'ongoing'
  };

  if (editingMatch.value) {
    updateMatch(editingMatch.value.id, newMatchData);
  } else {
    addMatch(newMatchData);
  }

  closeModals();
};

const handleFinalizeMatch = (finalizeData) => {
  if (!selectedMatch.value) return;

  const match = selectedMatch.value;
  const event = state.events.find(e => e.id === match.eventId);
  let winner = null;

  if (event?.thresholdIncremental && finalizeData.setScores.length > 0) {
    if (match.matchupType === '1v1') {
      let teamAWins = 0;
      let teamBWins = 0;

      finalizeData.setScores.forEach(set => {
        if (set.teamA > set.teamB) teamAWins++;
        else if (set.teamB > set.teamA) teamBWins++;
      });

      winner = teamAWins > teamBWins ? match.teamAId : match.teamBId;

      finalizeMatch(match.id, {
        scores: { teamA: teamAWins, teamB: teamBWins },
        setScores: finalizeData.setScores,
        status: 'completed',
        winner
      });

      if (winner) updateTeamWins(winner, 1);
    } else {
      const totals = {};
      match.participants?.forEach(p => {
        totals[p] = 0;
        finalizeData.setScores.forEach(set => {
          let maxScore = -1;
          let setWinner = null;
          match.participants?.forEach(part => {
            if (set[part] > maxScore) {
              maxScore = set[part];
              setWinner = part;
            }
          });
          if (setWinner) {
            totals[setWinner] = (totals[setWinner] || 0) + 1;
          }
        });
      });

      let maxWins = -1;
      match.participants?.forEach(p => {
        if (totals[p] > maxWins) {
          maxWins = totals[p];
          winner = p;
        }
      });

      const finalScores = {};
      match.participants?.forEach(p => {
        finalScores[p] = finalizeData.setScores.reduce((sum, set) => sum + (set[p] || 0), 0);
      });

      finalizeMatch(match.id, {
        scores: finalScores,
        setScores: finalizeData.setScores,
        status: 'completed',
        winner
      });

      if (winner) updateTeamWins(winner, 1);
    }
  } else {
    if (match.matchupType === '1v1') {
      const scoreA = parseInt(finalizeData.scores.teamA) || 0;
      const scoreB = parseInt(finalizeData.scores.teamB) || 0;
      const isTimeRanked = event?.scoringSystemId === 3;

      if (isTimeRanked) {
        winner = scoreA < scoreB ? match.teamAId : match.teamBId;
      } else {
        winner = scoreA > scoreB ? match.teamAId : match.teamBId;
      }

      finalizeMatch(match.id, {
        scores: { teamA: scoreA, teamB: scoreB },
        status: 'completed',
        winner
      });

      if (winner) updateTeamWins(winner, 1);
    } else {
      let maxScore = -1;
      match.participants?.forEach(p => {
        const score = parseInt(finalizeData.scores[p]) || 0;
        if (score > maxScore) {
          maxScore = score;
          winner = p;
        }
      });

      finalizeMatch(match.id, {
        scores: finalizeData.scores,
        status: 'completed',
        winner
      });

      if (winner) updateTeamWins(winner, 1);
    }
  }

  closeModals();
};

const deleteMatchHandler = (id) => {
  if (confirm('Delete this match?')) {
    deleteMatch(id);
  }
};
</script>

<template>
  <div class="page-container">
    <header class="dashboard-header">
      <div class="welcome-text">
        <h1>Matches Management</h1>
        <p>Create and manage matches, input scores, and finalize results.</p>
      </div>
      <div class="header-actions">
        <button class="btn-primary" @click="openMatchModal()">
          <i class="fas fa-plus"></i> Create New Match
        </button>
      </div>
    </header>

    <!-- Ongoing Matches -->
    <section class="matches-section">
      <h2 class="section-title">
        <i class="fas fa-broadcast-tower"></i>
        Ongoing Matches
      </h2>
      <div class="matches-grid">
        <MatchCard
          v-for="match in ongoingMatches"
          :key="match.id"
          :match="match"
          :event="getEvent(match.eventId)"
          :teams="state.teams"
          @finalize="openFinalizeModal"
          @delete="deleteMatchHandler"
        />
        <div v-if="ongoingMatches.length === 0" class="no-matches">
          <i class="fas fa-calendar-times"></i>
          <p>No ongoing matches. Create a new match to get started.</p>
        </div>
      </div>
    </section>

    <!-- Completed Matches -->
    <section class="matches-section">
      <h2 class="section-title">
        <i class="fas fa-check-circle"></i>
        Completed Matches
      </h2>
      <div class="matches-grid">
        <MatchCard
          v-for="match in completedMatches"
          :key="match.id"
          :match="match"
          :event="getEvent(match.eventId)"
          :teams="state.teams"
        />
        <div v-if="completedMatches.length === 0" class="no-matches">
          <i class="fas fa-inbox"></i>
          <p>No completed matches yet.</p>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <MatchModal
      :show="showModal"
      :match="editingMatch"
      :events="state.events"
      :teams="state.teams"
      @close="closeModals"
      @save="handleSaveMatch"
    />

    <FinalizeMatchModal
      :show="showFinalizeModal"
      :match="selectedMatch"
      :event="selectedMatch ? getEvent(selectedMatch.eventId) : null"
      :teams="state.teams"
      @close="closeModals"
      @finalize="handleFinalizeMatch"
    />
  </div>
</template>

<style scoped>
.page-container {
  padding: 30px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

/* Sections */
.matches-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.2rem;
  color: var(--adnu-blue-navy);
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
}

.section-title i {
  color: var(--adnu-gold);
}

/* Matches Grid */
.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

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

/* No Matches */
.no-matches {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.no-matches i {
  font-size: 3rem;
  display: block;
  margin-bottom: 12px;
  opacity: 0.5;
}

.no-matches p {
  margin: 0;
  font-size: 0.95rem;
}

/* Modal */
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
  max-width: 550px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.match-modal { max-width: 550px; border-top: 6px solid var(--adnu-blue-dark); }
.finalize-modal { max-width: 600px; border-top: 6px solid var(--adnu-gold); }

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

.form-row {
  display: flex;
  gap: 15px;
}

.flex-1 {
  flex: 1;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  font-weight: 700;
  font-size: 0.75rem;
  color: var(--adnu-blue-navy);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-family: var(--font-main);
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.modal-input:focus {
  outline: none;
  border-color: var(--adnu-blue-dark);
}

/* Toggle Group */
.toggle-group {
  display: flex;
  gap: 10px;
}

.toggle-btn {
  flex: 1;
  padding: 12px 16px;
  background: var(--bg-gray-light);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.2s;
  font-family: var(--font-main);
}

.toggle-btn.active {
  background: var(--adnu-blue-dark);
  color: var(--white);
  border-color: var(--adnu-blue-dark);
}

/* Team Selection */
.team-selection {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.participant-selectors {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 250px;
  overflow-y: auto;
}

.participant-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: var(--bg-gray-light);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.participant-option:hover {
  border-color: var(--adnu-blue-dark);
}

.participant-option.selected {
  border-color: var(--adnu-gold);
  background: #FFF9E6;
}

.team-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.participant-option .team-name {
  flex: 1;
  font-weight: 600;
  font-size: 0.95rem;
}

.participant-option i {
  font-size: 1rem;
}

.participant-option.selected i {
  color: var(--adnu-gold);
}

/* Set Scores */
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
