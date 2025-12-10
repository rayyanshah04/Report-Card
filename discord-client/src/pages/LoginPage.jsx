import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import useToast from '../hooks/useToast';

export default function LoginPage() {
  const pushToast = useToast();
  const user = useAuthStore((state) => state.user);
  const login = useAuthStore((state) => state.login);
  const loading = useAuthStore((state) => state.loading);

  const [credentials, setCredentials] = useState({ username: '', password: '' });

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!credentials.username || !credentials.password) {
      pushToast({ type: 'warning', title: 'Missing info', message: 'Please enter both username and password.' });
      return;
    }

    try {
      await login(credentials.username, credentials.password);
      pushToast({ type: 'success', title: 'Welcome back', message: 'Authentication successful.' });
    } catch (error) {
      pushToast({ type: 'error', title: 'Login failed', message: error.message });
    }
  };

  if (user?.user_id) {
    return <Navigate to="/students" replace />;
  }

  return (
    <div className="login-screen">
      <div className="login-card glass-surface">
        <div className="login-branding">
          <p className="eyebrow">Faizan Academy</p>
          <h2>Report Studio</h2>
          <p className="muted">Sign in with your staff credentials to enter the Discord-quality console.</p>
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <label>
            <span>Username</span>
            <input
              className="input dark"
              type="text"
              value={credentials.username}
              onChange={(event) => setCredentials((prev) => ({ ...prev, username: event.target.value }))}
              placeholder="e.g., admin"
            />
          </label>
          <label>
            <span>Password</span>
            <input
              className="input dark"
              type="password"
              value={credentials.password}
              onChange={(event) => setCredentials((prev) => ({ ...prev, password: event.target.value }))}
              placeholder="••••••"
            />
          </label>
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? 'Authenticating…' : 'Enter Studio'}
          </button>
        </form>
      </div>
    </div>
  );
}
