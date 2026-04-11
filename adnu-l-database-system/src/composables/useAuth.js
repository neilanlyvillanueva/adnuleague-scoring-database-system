import { reactive, readonly, computed } from 'vue';

const state = reactive({
  user: null,
  isAuthenticated: false,
  isLoading: false
});

export const userRole = computed(() => state.user?.role || null);

const login = (username, password, role) => {
  state.isLoading = true;

  // Simulate API call - in production, this would hit your backend
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Simple validation - in production, validate against backend
      if (username && password && role) {
        state.user = {
          id: 1,
          username: username,
          role: role
        };
        state.isAuthenticated = true;
        state.isLoading = false;

        // Persist to localStorage
        localStorage.setItem('adnl_user', JSON.stringify(state.user));
        localStorage.setItem('adnl_auth', 'true');

        resolve(state.user);
      } else {
        state.isLoading = false;
        reject(new Error('Invalid credentials'));
      }
    }, 500);
  });
};

const logout = () => {
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
    checkAuth,
    isAuthenticated: () => state.isAuthenticated
  };
}
