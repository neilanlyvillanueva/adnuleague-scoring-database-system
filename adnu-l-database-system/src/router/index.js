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
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('adnl_auth') === 'true';
  const user = JSON.parse(localStorage.getItem('adnl_user') || '{}');
  const userRole = user.role;
  const requiresAuth = to.meta.requiresAuth !== false;
  const allowedRoles = to.meta.roles || ['admin', 'tabulation'];

  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.path === '/login' && isAuthenticated) {
    next('/dashboard');
  } else if (requiresAuth && isAuthenticated && !allowedRoles.includes(userRole)) {
    // User doesn't have permission for this route
    next('/dashboard');
  } else {
    next();
  }
});

export default router