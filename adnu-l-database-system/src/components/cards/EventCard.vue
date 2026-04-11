<script setup>
defineProps({
  event: {
    type: Object,
    required: true
  },
  scoringSystems: {
    type: Array,
    required: true
  }
});

defineEmits(['edit', 'delete']);

const getScoringSystemName = (id) => {
  return scoringSystems.find(s => s.id === id)?.name || 'Unknown';
};
</script>

<template>
  <div class="event-card">
    <div class="event-type-tag" :class="event.category.toLowerCase().replace(/\s+/g, '-')">
      {{ event.category }}
    </div>
    <div class="event-card-content">
      <div class="event-main">
        <h3>{{ event.name }}</h3>
        <div class="event-details">
          <span class="detail-badge">
            <i class="fas fa-trophy"></i>
            {{ getScoringSystemName(event.scoringSystemId) }}
          </span>
          <span v-if="event.matchupSystem" class="detail-badge">
            <i class="fas fa-users"></i>
            {{ event.matchupSystem === '1v1' ? 'Head-to-Head' : 'Free-for-All' }}
          </span>
          <span v-if="event.thresholdIncremental" class="detail-badge">
            <i class="fas fa-layer-group"></i>
            {{ event.sets }} Sets
          </span>
        </div>
      </div>
      <div class="event-footer">
        <div class="action-group">
          <button class="btn-icon edit" @click="$emit('edit', event)"><i class="fas fa-edit"></i></button>
          <button class="btn-icon delete" @click="$emit('delete', event.id)"><i class="fas fa-trash-alt"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.event-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: box-shadow 0.2s ease;
}

.event-card:hover {
  box-shadow: var(--shadow-md);
}

.event-type-tag {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 8px 15px;
  letter-spacing: 0.5px;
}

.event-type-tag.sports { background: #E8F0FF; color: var(--adnu-blue-dark); }
.event-type-tag.cultural { background: #FFF9E6; color: #B8860B; }
.event-type-tag.academic { background: #E8F5E9; color: #2E7D32; }
.event-type-tag.laro-ng-lahi { background: #FFF3E0; color: #E65100; }

.event-card-content { padding: 20px; }

.event-main h3 {
  margin: 0 0 12px 0;
  font-size: 1.15rem;
  color: var(--adnu-blue-navy);
  font-weight: 700;
}

.event-details {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.detail-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--bg-gray-light);
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.detail-badge i {
  font-size: 0.75rem;
}

.event-footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid var(--border-color);
  padding-top: 12px;
}

.action-group {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--white);
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 0.85rem;
}

.btn-icon:hover {
  transform: translateY(-1px);
}

.btn-icon.edit:hover {
  background: var(--adnu-blue-light);
  border-color: var(--adnu-blue-dark);
  color: var(--adnu-blue-dark);
}

.btn-icon.delete:hover {
  background: var(--adnu-danger-light);
  border-color: var(--adnu-danger);
  color: var(--adnu-danger);
}
</style>
