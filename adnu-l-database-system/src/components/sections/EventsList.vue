<script setup>
import EventCard from '../cards/EventCard.vue';

defineProps({
  events: {
    type: Array,
    required: true
  },
  scoringSystems: {
    type: Array,
    required: true
  },
  activeFilter: {
    type: String,
    required: true
  },
  categories: {
    type: Array,
    required: true
  }
});

defineEmits(['filter-change', 'edit-event', 'delete-event']);
</script>

<template>
  <div>
    <!-- Filter Bar -->
    <div class="filter-bar">
      <button
        v-for="cat in categories"
        :key="cat"
        :class="['filter-btn', { active: activeFilter === cat }]"
        @click="$emit('filter-change', cat)"
      >
        {{ cat }}
      </button>
    </div>

    <!-- Events Grid -->
    <div class="events-grid">
      <EventCard
        v-for="event in events"
        :key="event.id"
        :event="event"
        :scoring-systems="scoringSystems"
        @edit="$emit('edit-event', event)"
        @delete="$emit('delete-event', event.id)"
      />
      <div v-if="events.length === 0" class="no-data">
        <i class="fas fa-calendar-times"></i>
        <p>No events found. Create your first event to get started.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Filter Bar */
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  background: var(--white);
  color: var(--text-muted);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
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

/* Events Grid */
.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
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
