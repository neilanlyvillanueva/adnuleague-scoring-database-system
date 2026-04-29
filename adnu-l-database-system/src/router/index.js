import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/dashboard/Dashboard.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'tabulation'] }
  },
  {
    path: '/events',
    name: 'Events',
    component: () => import('../views/events/Events.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'tabulation'], editableRoles: ['admin', 'tabulation'] }
  },
  {
    path: '/teams',
    name: 'Teams',
    component: () => import('../views/teams/Teams.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'tabulation'], editableRoles: ['admin'] }
  },
  {
    path: '/matches',
    name: 'Matches',
    component: () => import('../views/matches/Matches.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'tabulation'], editableRoles: ['admin', 'tabulation'] }
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: () => import('../views/leaderboard/Leaderboard.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'tabulation'], editableRoles: ['admin'] }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/history/History.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'tabulation'], editableRoles: ['admin'] }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for auth and role-based access
router.beforeEach((to, from) => {
  const isAuthenticated = localStorage.getItem('adnl_auth') === 'true';
  const user = JSON.parse(localStorage.getItem('adnl_user') || '{}');
  const userRole = user.role;

  // 1. Handle Login Page Access
  if (to.path === '/login') {
    if (isAuthenticated) {
      return '/dashboard'; // Already logged in? Skip login.
    }
    return true; // Not logged in? Show login.
  }

  // 2. Handle Protected Routes
  if (to.meta.requiresAuth) {
    // If not logged in, force to login page
    if (!isAuthenticated) {
      return '/login';
    }

    // Role-Based Access Control (RBAC)
    const allowedRoles = to.meta.roles || [];

    if (!allowedRoles.includes(userRole)) {
      console.warn(`Access denied for role: ${userRole}`);
      return '/dashboard'; // Redirect unauthorized roles to a safe page
    }
  }

  // 3. Proceed for all other cases
  return true;
});

export default router