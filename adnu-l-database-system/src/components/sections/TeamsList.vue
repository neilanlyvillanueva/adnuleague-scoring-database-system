<script setup>
import TeamCard from '../cards/TeamCard.vue';

defineProps({
  teams: {
    type: Array,
    required: true
  }
});

defineEmits(['edit-team', 'delete-team', 'manage-participation']);
</script>

<template>
  <div class="teams-grid">
    <TeamCard
      v-for="team in teams"
      :key="team.id"
      :team="team"
      @edit="$emit('edit-team', team)"
      @delete="$emit('delete-team', team.id)"
      @manage-participation="$emit('manage-participation', team)"
    />
    <div v-if="teams.length === 0" class="no-data">
      <i class="fas fa-users-slash"></i>
      <p>No teams registered yet. Add your first team to get started.</p>
    </div>
  </div>
</template>

<style scoped>
.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.no-data {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.no-data i {
  font-size: 3rem;
  display: block;
  margin-bottom: 12px;
  opacity: 0.5;
}

.no-data p {
  margin: 0;
  font-size: 0.95rem;
}
</style>
