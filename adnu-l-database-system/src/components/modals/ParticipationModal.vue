<script setup>
const props = defineProps({
  show: Boolean,
  team: Object,
  events: Array,
  participatingSports: Array
});

const emit = defineEmits(['close', 'toggle-participation']);

const isParticipating = (sportId) => {
  return props.participatingSports?.includes(sportId) || false;
};

const handleToggle = (sportId) => {
  emit('toggle-participation', sportId);
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content participation-modal">
      <div class="modal-header-section">
        <h3>Sport Participation</h3>
        <p class="modal-subtitle">
          Select which sports <strong>{{ team?.name }}</strong> will participate in.
        </p>
      </div>

      <div class="participation-grid">
        <div
          v-for="event in events"
          :key="event.id"
          :class="['sport-card', { selected: isParticipating(event.id) }]"
          @click="handleToggle(event.id)"
        >
          <div class="sport-card-header">
            <span class="sport-name">{{ event.name }}</span>
            <span class="sport-category">{{ event.category }}</span>
          </div>
          <div class="sport-card-footer">
            <span class="matchup-badge">{{ event.matchupSystem === '1v1' ? '1v1' : 'FFA' }}</span>
            <i :class="['participation-check', 'fas', isParticipating(event.id) ? 'fa-check-circle' : 'fa-circle']"></i>
          </div>
        </div>
        <div v-if="events.length === 0" class="no-events">
          <i class="fas fa-inbox"></i>
          <p>No events configured yet. Create events first.</p>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn-ghost" @click="emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border-top: 6px solid var(--adnu-gold);
}

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

.participation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  padding: 0 24px 24px 24px;
  max-height: 400px;
  overflow-y: auto;
}

.sport-card {
  padding: 16px;
  background: var(--bg-gray-light);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.sport-card:hover {
  border-color: var(--adnu-blue-dark);
  background: var(--adnu-blue-light);
}

.sport-card.selected {
  border-color: var(--adnu-gold);
  background: #FFF9E6;
}

.sport-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.sport-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--adnu-blue-navy);
}

.sport-category {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--text-muted);
  background: var(--white);
  padding: 3px 8px;
  border-radius: 4px;
}

.sport-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.matchup-badge {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--white);
  padding: 3px 8px;
  border-radius: 4px;
}

.participation-check {
  font-size: 1.2rem;
}

.sport-card.selected .participation-check {
  color: var(--adnu-gold);
}

.no-events {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
}

.no-events i {
  font-size: 3rem;
  display: block;
  margin-bottom: 12px;
}

.no-events p {
  margin: 0;
  font-size: 0.95rem;
}

.modal-actions {
  padding: 16px 24px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
