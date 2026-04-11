<script setup>
defineProps({
  team: {
    type: Object,
    required: true
  }
});

defineEmits(['edit', 'delete', 'manage-participation']);
</script>

<template>
  <div class="team-card">
    <div class="card-accent" :style="{ backgroundColor: team.color }"></div>
    <div class="team-card-body">
      <div class="team-icon" :style="{ color: team.color, backgroundColor: team.color + '15' }">
        <i class="fas fa-shield-alt"></i>
      </div>
      <div class="team-info">
        <h3>{{ team.name }}</h3>
        <p class="participation-count">
          <i class="fas fa-trophy"></i>
          Participating in {{ team.participatingSports?.length || 0 }} sports
        </p>
      </div>
    </div>
    <div class="team-card-actions">
      <button class="btn-icon participation" @click="$emit('manage-participation', team)" title="Manage Sport Participation">
        <i class="fas fa-clipboard-check"></i>
      </button>
      <button class="btn-icon edit" @click="$emit('edit', team)"><i class="fas fa-edit"></i></button>
      <button class="btn-icon delete" @click="$emit('delete', team.id)"><i class="fas fa-trash-alt"></i></button>
    </div>
  </div>
</template>

<style scoped>
.team-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.card-accent {
  height: 5px;
  width: 100%;
}

.team-card-body {
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.team-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.team-info h3 {
  margin: 0 0 6px 0;
  font-size: 1.1rem;
  color: var(--text-main);
  font-weight: 700;
}

.team-info p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.participation-count {
  display: flex;
  align-items: center;
  gap: 6px;
}

.participation-count i {
  font-size: 0.75rem;
  color: var(--adnu-gold);
}

.team-card-actions {
  border-top: 1px solid var(--border-color);
  padding: 12px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background: #fafafa;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 8px;
  border-radius: var(--radius-md);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: var(--bg-gray-light);
}

.btn-icon.edit:hover {
  color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
}

.btn-icon.delete:hover {
  color: var(--adnu-danger);
  background: var(--adnu-danger-light);
}

.btn-icon.participation:hover {
  color: var(--adnu-gold);
  background: #FFF9E6;
}
</style>
