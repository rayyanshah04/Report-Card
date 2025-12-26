import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import api, { setAuthContext } from '../services/api';

const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      loading: false,
      error: null,
      login: async (username, password) => {
        set({ loading: true, error: null });
        try {
          const response = await api.post('/auth/login', { username, password });
          setAuthContext(response.data);
          set({ user: response.data, loading: false });
          return response.data;
        } catch (error) {
          const message = error.response?.data?.detail || 'Unable to sign in';
          set({ error: message, loading: false });
          throw new Error(message);
        }
      },
      logout: () => {
        setAuthContext(null);
        set({ user: null });
      },
    }),
    {
      name: 'faizan-report-user', // storage name
      storage: createJSONStorage(() => localStorage), // use localStorage
      partialize: (state) => ({ user: state.user }), // only persist the 'user' state
      onRehydrateStorage: () => (state) => {
        if (state?.user) {
          setAuthContext(state.user);
        }
      },
    },
  ),
);

export default useAuthStore;

