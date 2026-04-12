import { reactive, readonly, ref } from 'vue';
import axios from 'axios';

const state = reactive({
  // Pre-defined event categories
  eventCategories: [
    'Sports',
    'Special Events',
    'Esports',
    'Board Games',
    'Laro ng Lahi',
    'LitMusDa',
    'Outside Events',
    'Indoor Games'
  ],

  // Events - fetched from backend
  events: [],

  // Scoring Systems - pre-defined types (static reference)
  scoringSystems: [
    { id: 1, name: 'Timed Incremental (1v1)', type: 'predefined', description: 'Highest final score wins within X time (e.g., Basketball, Football, Futsal)', matchupSystem: '1v1' },
    { id: 2, name: 'Ranked Incremental (1v1)', type: 'predefined', description: 'Highest score wins, no time limit (e.g., Scrabble, Billiards, Softball, Dodgeball)', matchupSystem: '1v1' },
    { id: 3, name: 'Ranked Incremental (FFA)', type: 'predefined', description: 'Highest score wins, no time limit (e.g., Sipa, Darts, Discus, Javelin, Long Jump, Shotput)', matchupSystem: 'free-for-all' },
    { id: 4, name: 'Threshold Incremental (1v1)', type: 'predefined', description: 'Most set wins, counted by final scores per set (e.g., Volleyball, Badminton)', matchupSystem: '1v1', requiresSets: true },
    { id: 5, name: 'Ranked Time (FFA)', type: 'predefined', description: 'Ranked by lowest TIME (e.g., Chinese garter, sack race, running, swimming)', matchupSystem: 'free-for-all' },
    { id: 6, name: 'Criteria Based (FFA)', type: 'predefined', description: 'Highest sum of scores from set criteria (must total 100 points)', matchupSystem: 'free-for-all', requiresCriteria: true },
    { id: 7, name: 'Judge Based (FFA)', type: 'predefined', description: 'Highest sum of scores from judges (similar to Criteria Based)', matchupSystem: 'free-for-all', requiresCriteria: true },
    { id: 8, name: 'Win/Lose (FFA)', type: 'predefined', description: 'Win or Lose (1 or 0) (e.g., Sungka, Tug of War, Esports)', matchupSystem: 'free-for-all' }
  ],

  // Teams - fetched from backend
  teams: [],

  // Matches - fetched from backend
  matches: [],

  // Leaderboard - fetched from backend
  leaderboard: []
});

const loading = ref({
  events: false,
  teams: false,
  matches: false,
  leaderboard: false
});

const error = ref(null);

// API fetch functions
const fetchEvents = async () => {
  loading.value.events = true;
  try {
    const response = await axios.get('/api/sports');
    state.events = response.data;
  } catch (err) {
    console.error('Failed to fetch events:', err);
    error.value = 'Failed to load events';
  } finally {
    loading.value.events = false;
  }
};

const fetchTeams = async () => {
  loading.value.teams = true;
  try {
    const response = await axios.get('/api/teams');
    console.log('Fetched teams - response.data:', response.data);
    console.log('Is array?', Array.isArray(response.data));
    console.log('Response type:', typeof response.data);
    // Ensure response.data is an array
    const teamsData = Array.isArray(response.data) ? response.data : [];
    console.log('Teams data to use:', teamsData);
    // Ensure reactivity by replacing the entire array
    state.teams.splice(0, state.teams.length, ...teamsData);
    console.log('State teams after update:', state.teams);
    console.log('State teams length:', state.teams.length);
  } catch (err) {
    console.error('Failed to fetch teams:', err);
    error.value = 'Failed to load teams';
  } finally {
    loading.value.teams = false;
  }
};

const fetchMatches = async () => {
  loading.value.matches = true;
  try {
    const response = await axios.get('/api/games');
    const matchesData = response.data.map(match => {
      // Convert backend scores {teamId: score} to frontend format {teamA, teamB} for 1v1
      let scores = {};
      if (match.matchupType === '1v1' || (match.sport && match.sport.matchup_type === '1v1')) {
        // For 1v1, convert teamId keys to teamA/teamB
        const teamIds = match.participants || Object.keys(match.scores || {}).map(Number);
        scores = {
          teamA: match.scores?.[teamIds[0]] ?? match.scores?.[teamIds[0]?.toString()] ?? 0,
          teamB: match.scores?.[teamIds[1]] ?? match.scores?.[teamIds[1]?.toString()] ?? 0
        };
      } else {
        // For FFA, keep teamId keys
        scores = match.scores || {};
      }

      return {
        ...match,
        eventId: match.eventId || match.sportId,
        matchupType: match.matchupType || match.sport?.matchup_type || '1v1',
        status: (match.status || 'ongoing').toLowerCase(),
        participants: match.participants || (match.results?.map(r => r.teamId) || []),
        teamAId: match.teamAId || match.participants?.[0],
        teamBId: match.teamBId || match.participants?.[1],
        scores
      };
    });
    // Ensure reactivity by replacing the entire array
    state.matches.splice(0, state.matches.length, ...matchesData);
  } catch (err) {
    console.error('Failed to fetch matches:', err);
    error.value = 'Failed to load matches';
  } finally {
    loading.value.matches = false;
  }
};

const fetchLeaderboard = async () => {
  loading.value.leaderboard = true;
  try {
    const response = await axios.get('/api/leaderboard');
    state.leaderboard = response.data;
  } catch (err) {
    console.error('Failed to fetch leaderboard:', err);
    error.value = 'Failed to load leaderboard';
  } finally {
    loading.value.leaderboard = false;
  }
};

// Fetch all data
const fetchAllData = async () => {
  await Promise.all([
    fetchEvents(),
    fetchTeams(),
    fetchMatches(),
    fetchLeaderboard()
  ]);
};

// Team operations
const addTeam = async (team) => {
  try {
    const response = await axios.post('/api/teams', { name: team.name, color: team.color });
    // Refresh teams list to ensure the new team is displayed
    await fetchTeams();
    return response.data;
  } catch (err) {
    console.error('Failed to add team:', err);
    throw new Error(err.response?.data?.error || 'Failed to add team');
  }
};

const updateTeam = async (id, updates) => {
  try {
    const response = await axios.put(`/api/teams/${id}`, updates);
    await fetchTeams();
    return response.data;
  } catch (err) {
    console.error('Failed to update team:', err);
    throw new Error(err.response?.data?.error || 'Failed to update team');
  }
};

const deleteTeam = async (id) => {
  try {
    await axios.delete(`/api/teams/${id}`);
    await fetchTeams();
  } catch (err) {
    console.error('Failed to delete team:', err);
    throw new Error(err.response?.data?.error || 'Failed to delete team');
  }
};

const toggleTeamSportParticipation = async (teamId, sportId) => {
  try {
    const response = await axios.post(`/api/teams/${teamId}/participation/${sportId}`);
    const index = state.teams.findIndex(t => t.id === teamId);
    if (index !== -1) {
      state.teams[index] = response.data.team;
    }
    return response.data;
  } catch (err) {
    console.error('Failed to toggle participation:', err);
    throw new Error(err.response?.data?.error || 'Failed to update participation');
  }
};

// Event/Sport operations
const addEvent = async (event) => {
  try {
    const criteria = event.criteria?.map(c => ({ name: c.name, points: c.points })) || [];
    const response = await axios.post('/api/sports', {
      name: event.name,
      category: event.category,
      scoringSystemId: event.scoringSystemId,
      matchupSystem: event.matchupSystem,
      sets: event.sets,
      criteria
    });
    state.events.push(response.data);
    return response.data;
  } catch (err) {
    console.error('Failed to add event:', err);
    throw new Error(err.response?.data?.error || 'Failed to add event');
  }
};

const updateEvent = async (id, updates) => {
  try {
    const criteria = updates.criteria?.map(c => ({ name: c.name, points: c.points })) || [];
    const response = await axios.put(`/api/sports/${id}`, { ...updates, criteria });
    const index = state.events.findIndex(e => e.id === id);
    if (index !== -1) {
      state.events[index] = response.data;
    }
    return response.data;
  } catch (err) {
    console.error('Failed to update event:', err);
    throw new Error(err.response?.data?.error || 'Failed to update event');
  }
};

const deleteEvent = async (id) => {
  try {
    await axios.delete(`/api/sports/${id}`);
    state.events = state.events.filter(e => e.id !== id);
  } catch (err) {
    console.error('Failed to delete event:', err);
    throw new Error(err.response?.data?.error || 'Failed to delete event');
  }
};

// Match operations
const addMatch = async (match) => {
  try {
    const payload = {
      eventId: match.eventId,
      matchupType: match.matchupType,
      teamAId: match.teamAId,
      teamBId: match.teamBId,
      participants: match.participants || [],
      venue: match.venue
    };
    const response = await axios.post('/api/games', payload);
    // Normalize the response data to match frontend expectations
    const newMatch = {
      ...response.data,
      eventId: response.data.eventId || response.data.sportId,
      matchupType: response.data.matchupType || '1v1',
      status: (response.data.status || 'ongoing').toLowerCase(),
      participants: response.data.participants || [],
      teamAId: response.data.teamAId || response.data.participants?.[0],
      teamBId: response.data.teamBId || response.data.participants?.[1],
      // Convert backend scores {teamId: score} to frontend format {teamA, teamB} for 1v1
      scores: (() => {
        const scores = response.data.scores || {};
        if (response.data.matchupType === '1v1') {
          const teamIds = response.data.participants || Object.keys(scores).map(Number);
          return {
            teamA: scores[teamIds[0]] ?? scores[teamIds[0]?.toString()] ?? 0,
            teamB: scores[teamIds[1]] ?? scores[teamIds[1]?.toString()] ?? 0
          };
        }
        return scores;
      })()
    };
    // Ensure reactivity by replacing the entire array
    state.matches.splice(0, 0, newMatch);
    return newMatch;
  } catch (err) {
    console.error('Failed to add match:', err);
    throw new Error(err.response?.data?.error || 'Failed to add match');
  }
};

const updateMatch = async (id, updates) => {
  try {
    // Note: Backend may not have a direct update endpoint, adjust as needed
    const index = state.matches.findIndex(m => m.id === id);
    if (index !== -1) {
      state.matches[index] = { ...state.matches[index], ...updates };
    }
    return updates;
  } catch (err) {
    console.error('Failed to update match:', err);
    throw new Error(err.response?.data?.error || 'Failed to update match');
  }
};

const finalizeMatch = async (id, finalData) => {
  try {
    const response = await axios.post(`/api/games/${id}/finalize`, finalData);
    const index = state.matches.findIndex(m => m.id === id);
    if (index !== -1) {
      // Normalize the response data to match frontend expectations
      const updatedMatch = {
        ...response.data,
        eventId: response.data.eventId || response.data.sportId,
        matchupType: response.data.matchupType || '1v1',
        status: (response.data.status || 'ongoing').toLowerCase(),
        participants: response.data.participants || [],
        teamAId: response.data.teamAId || response.data.participants?.[0],
        teamBId: response.data.teamBId || response.data.participants?.[1],
        // Convert backend scores {teamId: score} to frontend format {teamA, teamB} for 1v1
        scores: (() => {
          const scores = response.data.scores || {};
          if (response.data.matchupType === '1v1') {
            const teamIds = response.data.participants || Object.keys(scores).map(Number);
            return {
              teamA: scores[teamIds[0]] ?? scores[teamIds[0]?.toString()] ?? 0,
              teamB: scores[teamIds[1]] ?? scores[teamIds[1]?.toString()] ?? 0
            };
          }
          return scores;
        })()
      };
      state.matches[index] = updatedMatch;
    }
    // Refresh leaderboard after finalizing
    await fetchLeaderboard();
    return response.data;
  } catch (err) {
    console.error('Failed to finalize match:', err);
    throw new Error(err.response?.data?.error || 'Failed to finalize match');
  }
};

const deleteMatch = async (id) => {
  try {
    await axios.delete(`/api/games/${id}`);
    const index = state.matches.findIndex(m => m.id === id);
    if (index !== -1) {
      state.matches.splice(index, 1);
    }
  } catch (err) {
    console.error('Failed to delete match:', err);
    throw new Error(err.response?.data?.error || 'Failed to delete match');
  }
};

// Helper functions
const getEvent = (id) => state.events.find(e => e.id === id);
const getTeam = (id) => state.teams.find(t => t.id === id);
const getMatch = (id) => state.matches.find(m => m.id === id);
const getScoringSystem = (id) => state.scoringSystems.find(s => s.id === id);
const getScoringSystems = () => state.scoringSystems;

const getLeaderboard = () => {
  return [...state.leaderboard]
    .map(entry => {
      const team = state.teams.find(t => t.id === entry.teamId);
      return {
        ...entry,
        teamName: entry.teamName || team?.name || 'Unknown',
        teamColor: entry.teamColor || team?.color || '#ccc'
      };
    })
    .sort((a, b) => b.wins - a.wins);
};

// Legacy function - wins are now tracked on backend
const updateTeamWins = async (teamId, winsDelta) => {
  // Wins are automatically updated on the backend when matches are finalized
  // This function is kept for backwards compatibility but doesn't need to do anything
  console.log('Team wins updated:', teamId, winsDelta);
  await fetchLeaderboard();
};

const addScoringSystem = (system) => {
  // Scoring systems are predefined and static
  // This is kept for UI compatibility but doesn't persist to backend
  const newId = state.scoringSystems.length + 1;
  state.scoringSystems.push({ ...system, id: newId, type: 'custom' });
  return newId;
};

export function useStore() {
  return {
    state: readonly(state),
    loading: readonly(loading),
    error,
    scoringSystems: readonly(state.scoringSystems),
    // Data fetching
    fetchAllData,
    fetchEvents,
    fetchTeams,
    fetchMatches,
    fetchLeaderboard,
    // Event operations
    addEvent,
    updateEvent,
    deleteEvent,
    getEvent,
    // Scoring system operations
    addScoringSystem,
    getScoringSystem,
    getScoringSystems,
    // Team operations
    addTeam,
    updateTeam,
    deleteTeam,
    getTeam,
    toggleTeamSportParticipation,
    // Match operations
    addMatch,
    updateMatch,
    finalizeMatch,
    deleteMatch,
    getMatch,
    // Leaderboard operations
    updateTeamWins,
    getLeaderboard
  };
}
