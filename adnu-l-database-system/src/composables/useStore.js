import { reactive, readonly } from 'vue';

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

  // Events - each event has scoring configuration
  events: [
    {
      id: 1,
      name: "Men's Basketball",
      category: 'Sports',
      scoringSystemId: 1,
      matchupSystem: '1v1',
      sets: null,
      criteria: []
    },
    {
      id: 2,
      name: "Vocal Solo",
      category: 'LitMusDa',
      scoringSystemId: 6,
      matchupSystem: 'free-for-all',
      sets: null,
      criteria: [
        { name: 'Vocal Quality', points: 30 },
        { name: 'Stage Presence', points: 25 },
        { name: 'Interpretation', points: 25 },
        { name: 'Costume & Props', points: 20 }
      ]
    },
    {
      id: 3,
      name: "General Information Quiz",
      category: 'Academic',
      scoringSystemId: 8,
      matchupSystem: 'free-for-all',
      sets: null,
      criteria: []
    }
  ],

  // Scoring Systems - 8 pre-defined types
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
  const getScoringSystems = () => state.scoringSystems;

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
    scoringSystems: readonly(state.scoringSystems),
    addEvent,
    updateEvent,
    deleteEvent,
    getEvent,
    addScoringSystem,
    getScoringSystem,
    getScoringSystems,
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
