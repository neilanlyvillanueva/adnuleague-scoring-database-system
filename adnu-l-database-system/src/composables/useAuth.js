import { reactive, readonly, computed } from 'vue';

const API_BASE_URL = 'http://localhost:5000';

const state = reactive({
  user: null,
  isAuthenticated: false,
  isLoading: false
});

export const userRole = computed(() => state.user?.role || null);

const login = async (username, password, role) => {
  state.isLoading = true;

  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password, role })
    });

    const data = await response.json();

    if (!response.ok) {
      state.isLoading = false;
      throw new Error(data.error || 'Login failed');
    }

    state.user = data.user;
    state.isAuthenticated = true;
    state.isLoading = false;

    // Persist to localStorage
    localStorage.setItem('adnl_user', JSON.stringify(state.user));
    localStorage.setItem('adnl_auth', 'true');
    localStorage.setItem('adnl_token', data.access_token);

    return state.user;
  } catch (error) {
    state.isLoading = false;
    throw error;
  }
};

const logout = async () => {
  try {
    const token = localStorage.getItem('adnl_token');
    if (token) {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
    }
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    state.user = null;
    state.isAuthenticated = false;
    localStorage.removeItem('adnl_user');
    localStorage.removeItem('adnl_auth');
    localStorage.removeItem('adnl_token');
  }
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
    checkAuth,
    isAuthenticated: () => state.isAuthenticated
  };
}
