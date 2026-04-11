import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/dashboard/Dashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/events',
    name: 'Events',
    component: () => import('../views/events/Events.vue')
  },
  {
    path: '/teams',
    name: 'Teams',
    component: () => import('../views/teams/Teams.vue')
  },
  {
    path: '/matches',
    name: 'Matches',
    component: () => import('../views/matches/Matches.vue')
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: () => import('../views/leaderboard/Leaderboard.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router