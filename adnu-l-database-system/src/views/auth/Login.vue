<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../../composables/useAuth';
import { useStore } from '../../composables/useStore';

const router = useRouter();
const { login, state: authState } = useAuth();
const { fetchAllData, state: storeState } = useStore();

const form = reactive({
  username: '',
  password: '',
  role: ''
});

const error = ref('');
const showPassword = ref(false);
const isLoading = ref(false);

const handleSubmit = async () => {
  error.value = '';

  if (!form.username.trim() || !form.password.trim()) {
    error.value = 'Please enter both username and password';
    return;
  }

  if (!form.role) {
    error.value = 'Please select your role';
    return;
  }

  isLoading.value = true;

  try {
    await login(form.username, form.password, form.role);
    // Fetch all data after successful login
    await fetchAllData();
    router.push('/dashboard');
  } catch (err) {
    error.value = err.message || 'Invalid username or password';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-page">
    <div class="login-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="logo-container">
            <div class="logo-icon">
              <i class="fas fa-trophy"></i>
            </div>
          </div>
          <h1 class="app-title">ADNU SDBS</h1>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="username">
              <i class="fas fa-user"></i>
              Username
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input"
              placeholder="Enter your username"
              :disabled="isLoading"
              autocomplete="username"
            />
          </div>

          <div class="form-group">
            <label for="password">
              <i class="fas fa-lock"></i>
              Password
            </label>
            <div class="password-input-wrapper">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Enter your password"
                :disabled="isLoading"
                autocomplete="current-password"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                tabindex="-1"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </div>

          <div class="form-group">
            <label>
              <i class="fas fa-badge"></i>
              Select Role
            </label>
            <div class="role-selector">
              <button
                type="button"
                :class="['role-btn', { active: form.role === 'admin' }]"
                @click="form.role = 'admin'"
              >
                <i class="fas fa-user-shield"></i>
                Admin
              </button>
              <button
                type="button"
                :class="['role-btn', { active: form.role === 'tabulation' }]"
                @click="form.role = 'tabulation'"
              >
                <i class="fas fa-clipboard-list"></i>
                Tabulations Committee
              </button>
            </div>
          </div>

          <div v-if="error" class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            {{ error }}
          </div>

          <button type="submit" class="login-btn" :disabled="isLoading">
            <span v-if="!isLoading">
              <i class="fas fa-sign-in-alt"></i>
              Sign In
            </span>
            <span v-else class="loading-spinner">
              <i class="fas fa-circle-notch fa-spin"></i>
              Signing in...
            </span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  background: linear-gradient(135deg, #001F5C 0%, #0038A8 100%);
}

/* Animated Background */
.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s infinite ease-in-out;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: #FFD700;
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: #FF4D4D;
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: #E8F0FF;
  top: 50%;
  left: 50%;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

/* Login Container */
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  max-width: 450px;
  width: 100%;
  position: relative;
  z-index: 10;
}

/* Login Card */
.login-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

/* Header */
.login-header {
  text-align: center;
  margin-bottom: 35px;
}

.logo-container {
  margin-bottom: 20px;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #0038A8 0%, #001F5C 100%);
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 56, 168, 0.3);
}

.logo-icon i {
  font-size: 2.5rem;
  color: #FFD700;
}

.app-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #001F5C;
  margin: 0;
  letter-spacing: -0.5px;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  color: #001F5C;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group label i {
  color: #0038A8;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #E2E8F0;
  border-radius: 12px;
  font-size: 1rem;
  font-family: 'Montserrat', sans-serif;
  transition: all 0.2s;
  box-sizing: border-box;
  background: #FFFFFF;
}

.form-input:focus {
  outline: none;
  border-color: #0038A8;
  box-shadow: 0 0 0 4px rgba(0, 56, 168, 0.1);
}

.form-input:disabled {
  background: #F4F7FA;
  cursor: not-allowed;
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-wrapper .form-input {
  padding-right: 50px;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #718096;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #0038A8;
}

/* Error Message */
.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #FEE2E2;
  border: 1px solid #FECACA;
  border-radius: 10px;
  color: #AA3333;
  font-size: 0.9rem;
  font-weight: 500;
}

.error-message i {
  font-size: 1.1rem;
}

/* Login Button */
.login-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #0038A8 0%, #001F5C 100%);
  border: none;
  border-radius: 12px;
  color: #FFFFFF;
  font-size: 1rem;
  font-weight: 700;
  font-family: 'Montserrat', sans-serif;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(0, 56, 168, 0.3);
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 56, 168, 0.4);
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner i {
  margin-right: 8px;
}

/* Role Selector */
.role-selector {
  display: flex;
  gap: 12px;
}

.role-btn {
  flex: 1;
  padding: 14px 16px;
  background: #F4F7FA;
  border: 2px solid #E2E8F0;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  color: #718096;
  transition: all 0.2s;
  font-family: 'Montserrat', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.role-btn i {
  font-size: 1rem;
}

.role-btn:hover {
  border-color: #0038A8;
  color: #0038A8;
}

.role-btn.active {
  background: linear-gradient(135deg, #0038A8 0%, #001F5C 100%);
  color: #FFFFFF;
  border-color: #0038A8;
  box-shadow: 0 4px 12px rgba(0, 56, 168, 0.3);
}

.role-btn.active i {
  color: #FFD700;
}

/* Responsive */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 25px;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .logo-icon {
    width: 60px;
    height: 60px;
  }

  .logo-icon i {
    font-size: 2rem;
  }

  .login-features {
    gap: 10px;
  }

  .feature-item {
    font-size: 0.8rem;
    padding: 8px 12px;
  }
}
</style>
