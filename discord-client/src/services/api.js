import axios from 'axios';

const STORAGE_KEY = 'faizan-api-base';
const hostname = typeof window !== 'undefined' && window.location.hostname ? window.location.hostname : '127.0.0.1';
export const DEFAULT_API_BASE = import.meta.env.VITE_API_BASE || `http://${hostname}:8000`;

export function getApiBase() {
  if (typeof localStorage === 'undefined') return DEFAULT_API_BASE;
  return localStorage.getItem(STORAGE_KEY) || DEFAULT_API_BASE;
}

export function setApiBase(nextBase) {
  const value = nextBase?.trim() || DEFAULT_API_BASE;
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, value);
  }
  api.defaults.baseURL = value;
  return value;
}

const api = axios.create({
  baseURL: getApiBase(),
  timeout: 15000,
});

export default api;

export function setAuthContext(user) {
  const role = user?.role || '';
  const name = user?.username || '';
  api.defaults.headers.common['x-user-role'] = role;
  api.defaults.headers.common['x-user-name'] = name;
}
