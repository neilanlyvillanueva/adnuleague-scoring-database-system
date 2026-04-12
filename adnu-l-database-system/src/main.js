import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Set base URL for API requests
axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Request interceptor for auth token
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('adnl_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Clear auth and redirect to login
      localStorage.removeItem('adnl_user')
      localStorage.removeItem('adnl_auth')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)
app.use(router)
app.mount('#app')
