import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/dashboard/Dashboard.vue'

// For now, we'll use placeholder components for the others 
// or you can create the files in your views folder
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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router