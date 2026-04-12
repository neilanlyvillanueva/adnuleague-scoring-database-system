import { reactive, readonly, computed } from 'vue';
import axios from 'axios';

const state = reactive({
  user: null,
  isAuthenticated: false,
  isLoading: false
});

export const userRole = computed(() => state.user?.role || null);

const login = async (username, password, role) => {
  state.isLoading = true;

  try {
    const response = await axios.post('/auth/login', { username, password, role });

    state.isLoading = false;
    state.user = response.data.user;
    state.isAuthenticated = true;

    // Persist to localStorage
    localStorage.setItem('adnl_user', JSON.stringify(state.user));
    localStorage.setItem('adnl_auth', 'true');

    return state.user;
  } catch (error) {
    state.isLoading = false;
    throw new Error(error.response?.data?.error || 'Login failed');
  }
};

const logout = async () => {
  try {
    await axios.post('/auth/logout');
  } catch (error) {
    console.error('Logout error:', error);
  }
};

const clearAuthState = () => {
  state.user = null;
  state.isAuthenticated = false;
  localStorage.removeItem('adnl_user');
  localStorage.removeItem('adnl_auth');
};

const checkAuth = () => {
  const storedUser = localStorage.getItem('adnl_user');
  const isAuth = localStorage.getItem('adnl_auth') === 'true';

  if (storedUser && isAuth) {
    state.user = JSON.parse(storedUser);
    state.isAuthenticated = true;
  }
};

export function useAuth() {
  // Check auth on initialization
  checkAuth();

  return {
    state: readonly(state),
    userRole: readonly(userRole),
    login,
    logout,
    clearAuthState,
    checkAuth,
    isAuthenticated: () => state.isAuthenticated
  };
}
