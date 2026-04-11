<script setup>
import { ref, computed } from 'vue';
import { useStore } from '../../composables/useStore';
import { useAuth } from '../../composables/useAuth';

const { userRole } = useAuth();
const isAdmin = computed(() => userRole.value === 'admin');

const { state } = useStore();

const filterType = ref('all'); // all, completed, ongoing
const searchQuery = ref('');

const matchesWithDetails = computed(() => {
  return state.matches.map(match => {
    const event = state.events.find(e => e.id === match.eventId);
    const getTeamName = (id) => state.teams.find(t => t.id === id)?.name || 'Unknown';
    const getTeamColor = (id) => state.teams.find(t => t.id === id)?.color || '#ccc';

    let participants = [];
    if (match.matchupType === '1v1') {
      participants = [
        { id: match.teamAId, name: getTeamName(match.teamAId), color: getTeamColor(match.teamAId), score: match.scores?.teamA || 0 },
        { id: match.teamBId, name: getTeamName(match.teamBId), color: getTeamColor(match.teamBId), score: match.scores?.teamB || 0 }
      ];
    } else {
      participants = match.participants?.map(id => ({
        id,
        name: getTeamName(id),
        color: getTeamColor(id),
        score: match.scores?.[id] || 0
      })) || [];
    }

    return {
      ...match,
      eventName: event?.name || 'Unknown Event',
      eventCategory: event?.category || 'Unknown',
      participants,
      winner: match.winner
    };
  });
});

const filteredMatches = computed(() => {
  let filtered = matchesWithDetails.value;

  // Filter by type
  if (filterType.value === 'ongoing') {
    filtered = filtered.filter(m => m.status === 'ongoing');
  } else if (filterType.value === 'completed') {
    filtered = filtered.filter(m => m.status === 'completed');
  }

  // Filter by search
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(m =>
      m.eventName.toLowerCase().includes(query) ||
      m.participants.some(p => p.name.toLowerCase().includes(query))
    );
  }

  return filtered;
});

const getWinnerName = (match) => {
  if (!match.winner) return null;
  const participant = match.participants.find(p => p.id === match.winner);
  return participant?.name || 'Unknown';
};
</script>

<template>
  <div class="page-container">
    <header class="dashboard-header">
      <div class="welcome-text">
        <h1>Match History</h1>
        <p>View all matches, past and present, with detailed results.</p>
      </div>
    </header>

    <!-- Filters -->
    <div class="filters-section">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Search by event or team..."
        />
      </div>

      <div class="filter-buttons">
        <button
          :class="['filter-btn', { active: filterType === 'all' }]"
          @click="filterType = 'all'"
        >
          <i class="fas fa-list"></i> All
        </button>
        <button
          :class="['filter-btn', { active: filterType === 'ongoing' }]"
          @click="filterType = 'ongoing'"
        >
          <i class="fas fa-circle live-dot"></i> Ongoing
        </button>
        <button
          :class="['filter-btn', { active: filterType === 'completed' }]"
          @click="filterType = 'completed'"
        >
          <i class="fas fa-check-circle"></i> Completed
        </button>
      </div>
    </div>

    <!-- Stats Summary -->
    <div class="stats-summary">
      <div class="stat-item">
        <div class="stat-icon total">
          <i class="fas fa-calendar-alt"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ state.matches.length }}</span>
          <span class="stat-label">Total Matches</span>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon ongoing">
          <i class="fas fa-broadcast-tower"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ state.matches.filter(m => m.status === 'ongoing').length }}</span>
          <span class="stat-label">Ongoing</span>
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-icon completed">
          <i class="fas fa-flag-checkered"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ state.matches.filter(m => m.status === 'completed').length }}</span>
          <span class="stat-label">Completed</span>
        </div>
      </div>
    </div>

    <!-- Matches List -->
    <div class="matches-list">
      <div
        v-for="match in filteredMatches"
        :key="match.id"
        :class="['match-item', match.status]"
      >
        <div class="match-header">
          <div class="event-info">
            <span class="event-name">{{ match.eventName }}</span>
            <span class="event-category">{{ match.eventCategory }}</span>
          </div>
          <div class="match-meta">
            <span :class="['status-badge', match.status]">
              <i :class="match.status === 'ongoing' ? 'fas fa-circle live-dot' : 'fas fa-check-circle'"></i>
              {{ match.status === 'ongoing' ? 'LIVE' : 'Completed' }}
            </span>
            <span class="venue-info">
              <i class="fas fa-map-marker-alt"></i> {{ match.venue }}
            </span>
          </div>
        </div>

        <div class="match-body">
          <div class="participants-list">
            <div
              v-for="participant in match.participants"
              :key="participant.id"
              :class="['participant-row', { winner: match.winner === participant.id }]"
            >
              <div class="participant-info">
                <span class="team-color-dot" :style="{ backgroundColor: participant.color }"></span>
                <span class="participant-name">{{ participant.name }}</span>
              </div>
              <div class="participant-score">
                <span class="score-value">{{ participant.score }}</span>
                <i v-if="match.winner === participant.id" class="fas fa-trophy winner-icon"></i>
              </div>
            </div>
          </div>
        </div>

        <div v-if="match.status === 'completed' && match.winner" class="match-footer">
          <span class="winner-announcement">
            <i class="fas fa-trophy"></i>
            Winner: <strong>{{ getWinnerName(match) }}</strong>
          </span>
        </div>
      </div>

      <div v-if="filteredMatches.length === 0" class="no-matches">
        <i class="fas fa-inbox"></i>
        <p>No matches found.</p>
        <span v-if="searchQuery || filterType !== 'all'" class="clear-hint">
          Try adjusting your filters
        </span>
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

/* Filters Section */
.filters-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 15px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--white);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 10px 16px;
  min-width: 280px;
}

.search-box i {
  color: var(--text-muted);
}

.search-input {
  border: none;
  outline: none;
  flex: 1;
  font-size: 0.95rem;
  color: var(--text-main);
  font-family: var(--font-main);
}

.filter-buttons {
  display: flex;
  gap: 10px;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: var(--white);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: var(--bg-gray-light);
  border-color: var(--adnu-blue-dark);
}

.filter-btn.active {
  background: var(--adnu-blue-dark);
  color: var(--white);
  border-color: var(--adnu-blue-dark);
}

.live-dot {
  color: var(--adnu-live-red);
  font-size: 0.6rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Stats Summary */
.stats-summary {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  background: var(--white);
  padding: 20px 25px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
}

.stat-icon.total { background: var(--adnu-blue-light); color: var(--adnu-blue-dark); }
.stat-icon.ongoing { background: #FFEBEB; color: var(--adnu-live-red); }
.stat-icon.completed { background: #FFF9E6; color: var(--adnu-gold); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
  font-weight: 600;
}

/* Matches List */
.matches-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.match-item {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  border-left: 4px solid var(--border-color);
  transition: box-shadow 0.2s;
}

.match-item:hover {
  box-shadow: var(--shadow-md);
}

.match-item.ongoing {
  border-left-color: var(--adnu-live-red);
}

.match-item.completed {
  border-left-color: var(--adnu-gold);
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: var(--bg-gray-light);
  border-bottom: 1px solid var(--border-color);
}

.event-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.event-name {
  font-weight: 700;
  font-size: 1rem;
  color: var(--adnu-blue-navy);
}

.event-category {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  background: var(--white);
  padding: 4px 10px;
  border-radius: 4px;
}

.match-meta {
  display: flex;
  align-items: center;
  gap: 15px;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.ongoing {
  background: #FFEBEB;
  color: var(--adnu-live-red);
}

.status-badge.completed {
  background: #E8F5E9;
  color: #2E7D32;
}

.venue-info {
  font-size: 0.85rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 5px;
}

.venue-info i {
  font-size: 0.7rem;
}

/* Match Body */
.match-body {
  padding: 20px;
}

.participants-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.participant-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-gray-light);
  border-radius: var(--radius-md);
  transition: all 0.2s;
}

.participant-row.winner {
  background: #FFF9E6;
  border: 1px solid var(--adnu-gold);
}

.participant-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.team-color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.participant-name {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-main);
}

.participant-score {
  display: flex;
  align-items: center;
  gap: 10px;
}

.score-value {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--adnu-blue-dark);
  min-width: 30px;
  text-align: right;
}

.winner-icon {
  color: var(--adnu-gold);
  font-size: 1.1rem;
}

/* Match Footer */
.match-footer {
  padding: 12px 20px;
  background: #fafafa;
  border-top: 1px solid var(--border-color);
}

.winner-announcement {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.winner-announcement i {
  color: var(--adnu-gold);
}

.winner-announcement strong {
  color: var(--adnu-blue-navy);
}

/* No Matches */
.no-matches {
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

.clear-hint {
  display: block;
  margin-top: 8px;
  font-size: 0.85rem;
  color: var(--adnu-blue-dark);
}

/* Responsive */
@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: auto;
  }

  .filter-buttons {
    justify-content: center;
  }

  .stats-summary {
    justify-content: center;
  }

  .match-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .match-meta {
    flex-wrap: wrap;
  }
}
</style>
