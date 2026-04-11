<script setup>
import { ref, reactive, computed } from 'vue';

const dynamicData = reactive({
  systemTitle: 'ADNL S3',
});

const navItems = ref([
  { name: 'Dashboard', path: '/dashboard', icon: 'fas fa-th-large' },
  { name: 'Events', path: '/events', icon: 'fas fa-clipboard-list' },
  { name: 'Teams', path: '/teams', icon: 'fas fa-chart-line' },
  { name: 'Scoring', path: '/scoring', icon: 'fas fa-users-cog' },
  { name: 'Matches', path: '/matches', icon: 'fas fa-sliders-h' },
  { name: 'History', path: '/history', icon: 'fas fa-history' }
]);

const isModalOpen = ref(false);
const currentEditingKey = ref('');
const tempEditValue = ref('');

// Collapsed state for sidebar
const isCollapsed = ref(false);

const openEditModal = (key) => {
  currentEditingKey.value = key;
  tempEditValue.value = dynamicData[key];
  isModalOpen.value = true;
};

const closeModal = () => { isModalOpen.value = false; };

const saveEdit = () => {
  if (tempEditValue.value.trim() !== '') {
    dynamicData[currentEditingKey.value] = tempEditValue.value;
  }
  closeModal();
};

const handleLogout = () => {
  console.log("Logging out...");
};

// Emit collapsed state to parent
const emit = defineEmits(['collapse-change']);

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
  emit('collapse-change', isCollapsed.value);
};
</script>

<template>
  <aside :class="['sidebar', { collapsed: isCollapsed }]">
    <div class="sidebar-header">
      <div class="brand-title" @click="openEditModal('System Title')">
        <h2 v-if="!isCollapsed">{{ dynamicData.systemTitle }} <span class="edit-icon"><i class="fa-solid fa-pen-to-square"></i></span></h2>
        <h2 v-else @click.stop="toggleCollapse" class="collapse-toggle"><i class="fa-solid fa-bars"></i></h2>
      </div>
      <button v-if="!isCollapsed" class="collapse-btn" @click="toggleCollapse" title="Collapse Sidebar">
        <i class="fa-solid fa-chevron-left"></i>
      </button>
    </div>

    <nav class="sidebar-nav">
      <ul>
        <li v-for="item in navItems" :key="item.name">
          <router-link :to="item.path" class="nav-link" :title="isCollapsed ? item.name : ''">
            <i :class="item.icon"></i>
            <span v-if="!isCollapsed">{{ item.name }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <div class="flex-spacer"></div>

    <div class="sidebar-footer">
      <div class="footer-divider" v-if="!isCollapsed"></div>
      <button class="logout-btn" @click="handleLogout" :title="isCollapsed ? 'Exit' : ''">
        <i class="fas fa-sign-out-alt"></i>
        <span v-if="!isCollapsed">Exit</span>
      </button>
    </div>

    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>Edit {{ currentEditingKey }}</h3>
        <input
          v-model="tempEditValue"
          type="text"
          class="modal-input"
          @keyup.enter="saveEdit"
        />
        <div class="modal-actions">
            <button class="btn-ghost" @click="closeModal">Cancel</button>

             <button class="btn-primary" @click="saveEdit">Save</button>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background-color: var(--adnu-blue-navy);
  color: var(--white);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  font-family: var(--font-main);
  box-shadow: var(--shadow-md);
  border-radius: 0 10px 10px 0;
  transition: width 0.3s ease;
  z-index: 100;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  padding: 20px 24px 20px 24px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar.collapsed .sidebar-header {
  padding: 20px 10px 20px 10px;
  justify-content: center;
}

.brand-title {
  display: flex;
  align-items: center;
  flex: 1;
}

.brand-title h2 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
  overflow: hidden;
}

.sidebar.collapsed .brand-title h2 {
  justify-content: center;
}

.brand-title h2.collapse-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-title h2.collapse-toggle i {
  font-size: 1.2rem;
  color: var(--adnu-blue-light);
}

/* Collapse Toggle Button */
.collapse-btn {
  background: transparent;
  border: none;
  color: var(--adnu-blue-light);
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  opacity: 0.7;
  flex-shrink: 0;
  margin-left: 8px;
}

.collapse-btn:hover {
  opacity: 1;
  background-color: var(--adnu-blue-dark);
}

.sidebar.collapsed .collapse-btn {
  display: none;
}

/* Centering Logic */
.flex-spacer {
  flex-grow: 1;
}

.sidebar-nav {
  padding: 20px 0;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  color: var(--adnu-blue-light);
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
}

.sidebar.collapsed .nav-link {
  padding: 16px 10px;
  justify-content: center;
}

.nav-link i {
  margin-right: 16px;
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.sidebar.collapsed .nav-link i {
  margin-right: 0;
}

.nav-link:hover {
  background-color: var(--adnu-blue-dark);
  color: var(--white);
  padding-left: 28px;
}

.sidebar.collapsed .nav-link:hover {
  padding-left: 10px;
}

.router-link-active {
  color: var(--white) !important;
  background-color: var(--adnu-blue-dark);
}

.router-link-active span {
  position: relative;
  display: inline-block;
}

.router-link-active span::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--adnu-gold);
}

.sidebar.collapsed .router-link-active span::after {
  display: none;
}

.sidebar.collapsed .router-link-active {
  border-left: 3px solid var(--adnu-gold);
}

/* Footer & Logout Alignment */
.sidebar-footer {
  padding: 0 24px 30px 24px;
}

.sidebar.collapsed .sidebar-footer {
  padding: 0 10px 30px 10px;
}

.footer-divider {
  height: 1px;
  background-color: var(--border-color);
  opacity: 0.15;
  margin-bottom: 20px;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 12px 0;
  background: transparent;
  border: none;
  color: var(--adnu-blue-light);
  cursor: pointer;
  font-family: var(--font-main);
  font-size: 1rem;
  transition: color 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
}

.sidebar.collapsed .logout-btn {
  justify-content: center;
  padding: 12px 10px;
}

.logout-btn i {
  margin-right: 16px;
  width: 24px;
  flex-shrink: 0;
}

.sidebar.collapsed .logout-btn i {
  margin-right: 0;
}

.logout-btn:hover {
  color: var(--adnu-danger);
}

.brand-title i:hover {
    color: var(--adnu-gold);
}
.edit-icon {
    font-size: 0.8rem; opacity: 0.3;
    margin-left: 15px;
 }

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 31, 92, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--white);
  color: var(--text-main);
  padding: 24px;
  border-radius: var(--radius-lg);
  width: 300px;
  box-shadow: var(--shadow-md);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.1rem;
  color: var(--adnu-blue-dark);
}

.modal-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 1rem;
  box-sizing: border-box;
  font-family: var(--font-main);
  color: var(--text-main);
}

.modal-input:focus {
  outline: none;
  border-color: var(--adnu-blue-dark);
  box-shadow: 0 0 0 2px var(--adnu-blue-light);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-save {
    background: var(--adnu-blue-light);
    color: var(--adnu-blue-dark);
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}

.btn-cancel {
    background: var(--adnu-danger);
    color: var(--adnu-live-red);
    border: 1px solid var(--adnu-danger);
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}

.btn-save:hover {
    color: var(--adnu-blue-light);
    background: var(--adnu-blue-dark);
}

.btn-cancel:hover {
    background: var(--adnu-danger-strong);
    color: var(--white);
}
</style>