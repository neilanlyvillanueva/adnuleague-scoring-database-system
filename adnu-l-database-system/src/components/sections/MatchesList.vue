<script setup>
import MatchCard from '../cards/MatchCard.vue';
import MatchCard from '../cards/MatchCard.vue';

defineProps({
  matches: {
    type: Array,
    required: true
  },
  teams: {
    type: Array,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  iconClass: {
    type: String,
    required: true
  }
});

defineEmits(['finalize-match', 'delete-match']);

const getEvent = (eventId) => {
  // Event will be passed individually per match
  return null;
};
</script>

<template>
  <section class="matches-section">
    <h2 class="section-title">
      <i :class="iconClass"></i>
      {{ title }}
    </h2>
    <div class="matches-grid">
      <MatchCard
        v-for="match in matches"
        :key="match.id"
        :match="match"
        :event="$parent.getEvent?.(match.eventId) || {}"
        :teams="teams"
        @finalize="$emit('finalize-match', $event)"
        @delete="$emit('delete-match', $event)"
      />
      <div v-if="matches.length === 0" class="no-matches">
        <i class="fas fa-inbox"></i>
        <p>{{ title === 'Ongoing Matches' ? 'No ongoing matches. Create a new match to get started.' : 'No completed matches yet.' }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
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

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

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
</style>
