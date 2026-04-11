import { reactive, readonly } from 'vue';

const state = reactive({
  // Events (Sports) - each event has scoring configuration
  events: [
    {
      id: 1,
      name: "Men's Basketball",
      category: 'Sports',
      scoringSystemId: 1,
      thresholdIncremental: false,
      sets: null,
      matchupSystem: '1v1'
    },
    {
      id: 2,
      name: "Vocal Solo",
      category: 'Cultural',
      scoringSystemId: 2,
      thresholdIncremental: false,
      sets: null,
      matchupSystem: 'free-for-all'
    },
    {
      id: 3,
      name: "General Information Quiz",
      category: 'Academic',
      scoringSystemId: 1,
      thresholdIncremental: false,
      sets: null,
      matchupSystem: 'free-for-all'
    }
  ],

  // Scoring Systems - pre-defined and custom
  scoringSystems: [
    { id: 1, name: 'Point-based (Win/Loss)', type: 'predefined', description: 'Winner takes all, loser gets nothing' },
    { id: 2, name: 'Judged (Criteria)', type: 'predefined', description: 'Scored by judges based on criteria' },
    { id: 3, name: 'Timed (Race)', type: 'predefined', description: 'Lowest time wins' },
    { id: 4, name: 'Timed (Speed)', type: 'predefined', description: 'Highest value/score wins' }
  ],

  // Teams with sport participation
  teams: [
    { id: 1, name: 'Business & Accountancy', color: '#0038A8', participatingSports: [1, 2, 3] },
    { id: 2, name: 'Engineering', color: '#FFD700', participatingSports: [1, 2, 3] },
    { id: 3, name: 'Arts & Sciences', color: '#FF4D4D', participatingSports: [1, 3] },
    { id: 4, name: 'Computer Studies', color: '#1A202C', participatingSports: [1, 2, 3] }
  ],

  // Matches - ongoing and completed
  matches: [
    {
      id: 1,
      eventId: 1,
      matchupType: '1v1',
      teamAId: 1,
      teamBId: 2,
      participants: [],
      status: 'ongoing',
      scores: { teamA: 0, teamB: 0 },
      setScores: [],
      venue: 'Main Gymnasium'
    }
  ],

  // Leaderboard - win tallies per team
  leaderboard: [
    { teamId: 1, wins: 5 },
    { teamId: 2, wins: 3 },
    { teamId: 3, wins: 4 },
    { teamId: 4, wins: 2 }
  ]
});

export function useStore() {
  const addEvent = (event) => {
    const newId = state.events.length > 0 ? Math.max(...state.events.map(e => e.id)) + 1 : 1;
    state.events.push({ ...event, id: newId });
    return newId;
  };

  const updateEvent = (id, updates) => {
    const index = state.events.findIndex(e => e.id === id);
    if (index !== -1) {
      state.events[index] = { ...state.events[index], ...updates };
    }
  };

  const deleteEvent = (id) => {
    const index = state.events.findIndex(e => e.id === id);
    if (index !== -1) {
      state.events.splice(index, 1);
    }
  };

  const getEvent = (id) => state.events.find(e => e.id === id);

  // Scoring Systems
  const addScoringSystem = (system) => {
    const newId = state.scoringSystems.length > 0 ? Math.max(...state.scoringSystems.map(s => s.id)) + 1 : 1;
    state.scoringSystems.push({ ...system, id: newId, type: 'custom' });
    return newId;
  };

  const getScoringSystem = (id) => state.scoringSystems.find(s => s.id === id);

  // Teams
  const addTeam = (team) => {
    const newId = state.teams.length > 0 ? Math.max(...state.teams.map(t => t.id)) + 1 : 1;
    state.teams.push({ ...team, id: newId, participatingSports: team.participatingSports || [] });
    return newId;
  };

  const updateTeam = (id, updates) => {
    const index = state.teams.findIndex(t => t.id === id);
    if (index !== -1) {
      state.teams[index] = { ...state.teams[index], ...updates };
    }
  };

  const deleteTeam = (id) => {
    const index = state.teams.findIndex(t => t.id === id);
    if (index !== -1) {
      state.teams.splice(index, 1);
    }
  };

  const getTeam = (id) => state.teams.find(t => t.id === id);

  const toggleTeamSportParticipation = (teamId, sportId) => {
    const team = state.teams.find(t => t.id === teamId);
    if (team) {
      const index = team.participatingSports.indexOf(sportId);
      if (index === -1) {
        team.participatingSports.push(sportId);
      } else {
        team.participatingSports.splice(index, 1);
      }
    }
  };

  // Matches
  const addMatch = (match) => {
    const newId = state.matches.length > 0 ? Math.max(...state.matches.map(m => m.id)) + 1 : 1;
    state.matches.push({ ...match, id: newId, status: 'ongoing' });
    return newId;
  };

  const updateMatch = (id, updates) => {
    const index = state.matches.findIndex(m => m.id === id);
    if (index !== -1) {
      state.matches[index] = { ...state.matches[index], ...updates };
    }
  };

  const finalizeMatch = (id, finalData) => {
    const index = state.matches.findIndex(m => m.id === id);
    if (index !== -1) {
      state.matches[index] = { ...state.matches[index], ...finalData, status: 'completed' };
    }
  };

  const deleteMatch = (id) => {
    const index = state.matches.findIndex(m => m.id === id);
    if (index !== -1) {
      state.matches.splice(index, 1);
    }
  };

  const getMatch = (id) => state.matches.find(m => m.id === id);

  // Leaderboard
  const updateTeamWins = (teamId, winsDelta) => {
    const entry = state.leaderboard.find(l => l.teamId === teamId);
    if (entry) {
      entry.wins += winsDelta;
    } else {
      state.leaderboard.push({ teamId, wins: winsDelta });
    }
  };

  const getLeaderboard = () => {
    return [...state.leaderboard]
      .map(entry => {
        const team = state.teams.find(t => t.id === entry.teamId);
        return {
          ...entry,
          teamName: team?.name || 'Unknown',
          teamColor: team?.color || '#ccc'
        };
      })
      .sort((a, b) => b.wins - a.wins);
  };

  return {
    state: readonly(state),
    addEvent,
    updateEvent,
    deleteEvent,
    getEvent,
    addScoringSystem,
    getScoringSystem,
    addTeam,
    updateTeam,
    deleteTeam,
    getTeam,
    toggleTeamSportParticipation,
    addMatch,
    updateMatch,
    finalizeMatch,
    deleteMatch,
    getMatch,
    updateTeamWins,
    getLeaderboard
  };
}
