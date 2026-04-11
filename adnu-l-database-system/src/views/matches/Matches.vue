<script setup>
import { ref, reactive, computed } from 'vue';
import { useStore } from '../../composables/useStore';

const { state, addMatch, updateMatch, finalizeMatch, deleteMatch, updateTeamWins, getLeaderboard } = useStore();

const showModal = ref(false);
const showFinalizeModal = ref(false);
const showScoreModal = ref(false);
const isEditing = ref(false);
const editMatchId = ref(null);

// Form for creating new match
const matchForm = reactive({
  eventId: null,
  matchupType: '1v1',
  teamAId: null,
  teamBId: null,
  participants: [],
  venue: ''
});

// Form for finalizing match
const finalizeForm = reactive({
  scores: {},
  setScores: []
});

const selectedMatch = ref(null);

// Get teams participating in a specific event
const getParticipatingTeams = (eventId) => {
  return state.teams.filter(t => t.participatingSports?.includes(eventId));
};

const openMatchModal = (match = null) => {
  if (match) {
    isEditing.value = true;
    editMatchId.value = match.id;
    matchForm.eventId = match.eventId;
    matchForm.matchupType = match.matchupType;
    matchForm.teamAId = match.teamAId;
    matchForm.teamBId = match.teamBId;
    matchForm.participants = match.participants || [];
    matchForm.venue = match.venue || '';
  } else {
    isEditing.value = false;
    matchForm.eventId = null;
    matchForm.matchupType = '1v1';
    matchForm.teamAId = null;
    matchForm.teamBId = null;
    matchForm.participants = [];
    matchForm.venue = '';
  }
  showModal.value = true;
};

const openFinalizeModal = (match) => {
  selectedMatch.value = match;
  const event = state.events.find(e => e.id === match.eventId);

  finalizeForm.scores = {};
  finalizeForm.setScores = [];

  if (match.matchupType === '1v1') {
    finalizeForm.scores.teamA = 0;
    finalizeForm.scores.teamB = 0;
  } else {
    match.participants?.forEach(p => {
      finalizeForm.scores[p] = 0;
    });
  }

  // Initialize set scores if threshold incremental
  if (event?.thresholdIncremental && event.sets) {
    for (let i = 0; i < event.sets; i++) {
      if (match.matchupType === '1v1') {
        finalizeForm.setScores.push({ set: i + 1, teamA: 0, teamB: 0 });
      } else {
        const setScore = { set: i + 1 };
        match.participants?.forEach(p => {
          setScore[p] = 0;
        });
        finalizeForm.setScores.push(setScore);
      }
    }
  }

  showFinalizeModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  showFinalizeModal.value = false;
  showScoreModal.value = false;
  selectedMatch.value = null;
};

const saveMatch = () => {
  if (!matchForm.eventId) {
    alert('Please select an event/sport');
    return;
  }
  if (!matchForm.venue.trim()) {
    alert('Please enter a venue');
    return;
  }

  const event = state.events.find(e => e.id === matchForm.eventId);
  const participatingTeams = getParticipatingTeams(matchForm.eventId);

  if (matchForm.matchupType === '1v1') {
    if (!matchForm.teamAId || !matchForm.teamBId) {
      alert('Please select both teams');
      return;
    }
    if (matchForm.teamAId === matchForm.teamBId) {
      alert('Teams must be different');
      return;
    }
  } else {
    if (matchForm.participants.length < 2) {
      alert('Please select at least 2 participants for Free-for-All');
      return;
    }
  }

  const matchData = {
    eventId: matchForm.eventId,
    matchupType: matchForm.matchupType,
    teamAId: matchForm.teamAId,
    teamBId: matchForm.teamBId,
    participants: matchForm.participants,
    venue: matchForm.venue,
    scores: matchForm.matchupType === '1v1' ? { teamA: 0, teamB: 0 } : {},
    status: 'ongoing'
  };

  if (isEditing.value) {
    updateMatch(editMatchId.value, matchData);
  } else {
    addMatch(matchData);
  }

  closeModal();
};

const submitFinalScores = () => {
  if (!selectedMatch.value) return;

  const match = selectedMatch.value;
  const event = state.events.find(e => e.id === match.eventId);
  let winner = null;

  if (event?.thresholdIncremental && finalizeForm.setScores.length > 0) {
    // Count set wins for 1v1
    if (match.matchupType === '1v1') {
      let teamAWins = 0;
      let teamBWins = 0;

      finalizeForm.setScores.forEach(set => {
        if (set.teamA > set.teamB) teamAWins++;
        else if (set.teamB > set.teamA) teamBWins++;
      });

      winner = teamAWins > teamBWins ? match.teamAId : match.teamBId;

      finalizeMatch(match.id, {
        scores: { teamA: teamAWins, teamB: teamBWins },
        setScores: finalizeForm.setScores,
        status: 'completed',
        winner
      });

      if (winner) {
        updateTeamWins(winner, 1);
      }
    } else {
      // Free-for-all with sets - find participant with highest total
      const totals = {};
      match.participants?.forEach(p => {
        totals[p] = 0;
        finalizeForm.setScores.forEach(set => {
          // Find who won this set
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

      // Find overall winner
      let maxWins = -1;
      match.participants?.forEach(p => {
        if (totals[p] > maxWins) {
          maxWins = totals[p];
          winner = p;
        }
      });

      const finalScores = {};
      match.participants?.forEach(p => {
        finalScores[p] = finalizeForm.setScores.reduce((sum, set) => sum + (set[p] || 0), 0);
      });

      finalizeMatch(match.id, {
        scores: finalScores,
        setScores: finalizeForm.setScores,
        status: 'completed',
        winner
      });

      if (winner) {
        updateTeamWins(winner, 1);
      }
    }
  } else {
    // Non-set based scoring
    if (match.matchupType === '1v1') {
      const scoreA = parseInt(finalizeForm.scores.teamA) || 0;
      const scoreB = parseInt(finalizeForm.scores.teamB) || 0;

      const event = state.events.find(e => e.id === match.eventId);
      const isTimeRanked = event?.scoringSystemId === 3; // Timed (Race)

      if (isTimeRanked) {
        // Lowest time wins
        winner = scoreA < scoreB ? match.teamAId : match.teamBId;
      } else {
        // Highest score wins
        winner = scoreA > scoreB ? match.teamAId : match.teamBId;
      }

      finalizeMatch(match.id, {
        scores: { teamA: scoreA, teamB: scoreB },
        status: 'completed',
        winner
      });

      if (winner) {
        updateTeamWins(winner, 1);
      }
    } else {
      // Free-for-all - find highest score
      let maxScore = -1;
      match.participants?.forEach(p => {
        const score = parseInt(finalizeForm.scores[p]) || 0;
        if (score > maxScore) {
          maxScore = score;
          winner = p;
        }
      });

      finalizeMatch(match.id, {
        scores: finalizeForm.scores,
        status: 'completed',
        winner
      });

      if (winner) {
        updateTeamWins(winner, 1);
      }
    }
  }

  closeModal();
};

const deleteMatchHandler = (id) => {
  if (confirm('Delete this match?')) {
    deleteMatch(id);
  }
};

const toggleParticipant = (teamId) => {
  const index = matchForm.participants.indexOf(teamId);
  if (index === -1) {
    matchForm.participants.push(teamId);
  } else {
    matchForm.participants.splice(index, 1);
  }
};

const getTeamName = (id) => state.teams.find(t => t.id === id)?.name || 'Unknown';
const getTeamColor = (id) => state.teams.find(t => t.id === id)?.color || '#ccc';
const getEventName = (id) => state.events.find(e => e.id === id)?.name || 'Unknown';

const ongoingMatches = computed(() => state.matches.filter(m => m.status === 'ongoing'));
const completedMatches = computed(() => state.matches.filter(m => m.status === 'completed'));
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
        <div v-for="match in ongoingMatches" :key="match.id" class="match-card ongoing">
          <div class="match-header">
            <span class="event-badge">{{ getEventName(match.eventId) }}</span>
            <span class="venue-badge">
              <i class="fas fa-map-marker-alt"></i> {{ match.venue }}
            </span>
          </div>

          <div class="match-content">
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

            <div v-else class="matchup-ffa">
              <div v-for="participantId in match.participants" :key="participantId" class="ffa-participant">
                <span class="team-name" :style="{ color: getTeamColor(participantId) }">
                  {{ getTeamName(participantId) }}
                </span>
                <span class="team-score">{{ match.scores?.[participantId] || 0 }}</span>
              </div>
            </div>
          </div>

          <div class="match-actions">
            <button class="btn-sm btn-primary" @click="openFinalizeModal(match)">
              <i class="fas fa-check"></i> Finalize
            </button>
            <button class="btn-sm btn-ghost" @click="deleteMatchHandler(match.id)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>

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
        <div v-for="match in completedMatches" :key="match.id" class="match-card completed">
          <div class="match-header">
            <span class="event-badge">{{ getEventName(match.eventId) }}</span>
            <span class="venue-badge">
              <i class="fas fa-map-marker-alt"></i> {{ match.venue }}
            </span>
          </div>

          <div class="match-content">
            <div v-if="match.matchupType === '1v1'" class="matchup-1v1">
              <div class="team-side" :class="{ winner: match.winner === match.teamAId }">
                <span class="team-name" :style="{ color: getTeamColor(match.teamAId) }">
                  {{ getTeamName(match.teamAId) }}
                  <i v-if="match.winner === match.teamAId" class="fas fa-trophy winner-icon"></i>
                </span>
                <span class="team-score">{{ match.scores?.teamA || 0 }}</span>
              </div>
              <div class="vs-divider">VS</div>
              <div class="team-side" :class="{ winner: match.winner === match.teamBId }">
                <span class="team-name" :style="{ color: getTeamColor(match.teamBId) }">
                  {{ getTeamName(match.teamBId) }}
                  <i v-if="match.winner === match.teamBId" class="fas fa-trophy winner-icon"></i>
                </span>
                <span class="team-score">{{ match.scores?.teamB || 0 }}</span>
              </div>
            </div>

            <div v-else class="matchup-ffa">
              <div v-for="participantId in match.participants" :key="participantId"
                   class="ffa-participant" :class="{ winner: match.winner === participantId }">
                <span class="team-name" :style="{ color: getTeamColor(participantId) }">
                  {{ getTeamName(participantId) }}
                  <i v-if="match.winner === participantId" class="fas fa-trophy winner-icon"></i>
                </span>
                <span class="team-score">{{ match.scores?.[participantId] || 0 }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="completedMatches.length === 0" class="no-matches">
          <i class="fas fa-inbox"></i>
          <p>No completed matches yet.</p>
        </div>
      </div>
    </section>

    <!-- Create/Edit Match Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content match-modal">
        <div class="modal-header-section">
          <h3>{{ isEditing ? 'Edit Match' : 'Create New Match' }}</h3>
          <p class="modal-subtitle">Set up the match details and participants.</p>
        </div>

        <div class="modal-form-body">
          <div class="form-group">
            <label>Select Event / Sport</label>
            <select v-model="matchForm.eventId" class="modal-input">
              <option value="" disabled>Select an event...</option>
              <option v-for="event in state.events" :key="event.id" :value="event.id">
                {{ event.name }} ({{ event.matchupSystem }})
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Matchup Type</label>
            <div class="toggle-group">
              <button
                type="button"
                :class="['toggle-btn', { active: matchForm.matchupType === '1v1' }]"
                @click="matchForm.matchupType = '1v1'"
              >
                <i class="fas fa-versus"></i> 1v1 (Head-to-Head)
              </button>
              <button
                type="button"
                :class="['toggle-btn', { active: matchForm.matchupType === 'free-for-all' }]"
                @click="matchForm.matchupType = 'free-for-all'"
              >
                <i class="fas fa-users"></i> Free-for-All
              </button>
            </div>
          </div>

          <div class="form-group">
            <label>Venue</label>
            <input v-model="matchForm.venue" type="text" class="modal-input" placeholder="e.g. Main Gymnasium">
          </div>

          <!-- Team Selection for 1v1 -->
          <div v-if="matchForm.matchupType === '1v1' && matchForm.eventId" class="team-selection">
            <div class="form-row">
              <div class="form-group flex-1">
                <label>Team A</label>
                <select v-model="matchForm.teamAId" class="modal-input">
                  <option value="" disabled>Select Team A...</option>
                  <option v-for="team in getParticipatingTeams(matchForm.eventId)"
                          :key="team.id" :value="team.id">
                    {{ team.name }}
                  </option>
                </select>
              </div>
              <div class="form-group flex-1">
                <label>Team B</label>
                <select v-model="matchForm.teamBId" class="modal-input">
                  <option value="" disabled>Select Team B...</option>
                  <option v-for="team in getParticipatingTeams(matchForm.eventId)"
                          :key="team.id" :value="team.id">
                    {{ team.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Team Selection for Free-for-All -->
          <div v-if="matchForm.matchupType === 'free-for-all' && matchForm.eventId" class="team-selection">
            <label>Select Participants</label>
            <div class="participant-selectors">
              <div v-for="team in getParticipatingTeams(matchForm.eventId)"
                   :key="team.id"
                   :class="['participant-option', { selected: matchForm.participants.includes(team.id) }]"
                   @click="toggleParticipant(team.id)"
              >
                <span class="team-dot" :style="{ backgroundColor: team.color }"></span>
                <span class="team-name">{{ team.name }}</span>
                <i :class="['fas', matchForm.participants.includes(team.id) ? 'fa-check-circle' : 'fa-circle']"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-ghost" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveMatch">Create Match</button>
        </div>
      </div>
    </div>

    <!-- Finalize Scores Modal -->
    <div v-if="showFinalizeModal && selectedMatch" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content finalize-modal">
        <div class="modal-header-section">
          <h3>Finalize Match</h3>
          <p class="modal-subtitle">
            {{ getEventName(selectedMatch.eventId) }} - {{ selectedMatch.venue }}
          </p>
        </div>

        <div class="modal-form-body">
          <div v-if="state.events.find(e => e.id === selectedMatch.eventId)?.thresholdIncremental"
               class="set-scores-section">
            <h4>Set Scores</h4>

            <!-- 1v1 Set Scores -->
            <div v-if="selectedMatch.matchupType === '1v1'">
              <div v-for="(set, index) in finalizeForm.setScores" :key="index" class="set-row">
                <span class="set-label">Set {{ set.set }}</span>
                <div class="set-inputs">
                  <div class="team-input">
                    <span class="team-label">{{ getTeamName(selectedMatch.teamAId) }}</span>
                    <input type="number" v-model.number="set.teamA" class="score-input" min="0">
                  </div>
                  <span class="set-separator">-</span>
                  <div class="team-input">
                    <span class="team-label">{{ getTeamName(selectedMatch.teamBId) }}</span>
                    <input type="number" v-model.number="set.teamB" class="score-input" min="0">
                  </div>
                </div>
              </div>
              <div class="set-summary">
                <strong>Sets Won:</strong>
                <span>{{ getTeamName(selectedMatch.teamAId) }}: {{ finalizeForm.setScores.filter(s => s.teamA > s.teamB).length }}</span>
                <span>{{ getTeamName(selectedMatch.teamBId) }}: {{ finalizeForm.setScores.filter(s => s.teamB > s.teamA).length }}</span>
              </div>
            </div>

            <!-- FFA Set Scores -->
            <div v-else>
              <div v-for="(set, index) in finalizeForm.setScores" :key="index" class="set-row ffa-set">
                <span class="set-label">Set {{ set.set }}</span>
                <div class="ffa-set-inputs">
                  <div v-for="participantId in selectedMatch.participants" :key="participantId" class="team-input">
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

            <div v-if="selectedMatch.matchupType === '1v1'" class="score-row">
              <div class="team-input">
                <span class="team-label">{{ getTeamName(selectedMatch.teamAId) }}</span>
                <input type="number" v-model.number="finalizeForm.scores.teamA" class="score-input" min="0">
              </div>
              <span class="score-separator">-</span>
              <div class="team-input">
                <span class="team-label">{{ getTeamName(selectedMatch.teamBId) }}</span>
                <input type="number" v-model.number="finalizeForm.scores.teamB" class="score-input" min="0">
              </div>
            </div>

            <div v-else class="ffa-scores">
              <div v-for="participantId in selectedMatch.participants" :key="participantId" class="score-row">
                <span class="team-label">{{ getTeamName(participantId) }}</span>
                <input type="number" v-model.number="finalizeForm.scores[participantId]" class="score-input" min="0">
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-ghost" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="submitFinalScores">
            <i class="fas fa-check"></i> Confirm Results
          </button>
        </div>
      </div>
    </div>
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
