import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import useToast from '../hooks/useToast';
import api, { getApiBase, setApiBase } from '../services/api';

export default function LoginPage() {
  const pushToast = useToast();
  const user = useAuthStore((state) => state.user);
  const login = useAuthStore((state) => state.login);
  const loading = useAuthStore((state) => state.loading);

  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [connectionOpen, setConnectionOpen] = useState(false);
  const [serverInput, setServerInput] = useState(getApiBase());
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    if (!connectionOpen) {
      setServerInput(getApiBase());
      setHealthStatus(null);
    }
  }, [connectionOpen]);

  const handleTestConnection = async () => {
    try {
      const response = await api.get('/health');
      if (response.data?.status === 'ok') {
        setHealthStatus('ok');
        pushToast({ type: 'success', title: 'Connected', message: 'Server is reachable.' });
      } else {
        setHealthStatus('fail');
        pushToast({ type: 'error', title: 'Not ready', message: 'Server responded unexpectedly.' });
      }
    } catch (error) {
      setHealthStatus('fail');
      pushToast({
        type: 'error',
        title: 'Connection failed',
        message: error.response?.data?.detail || 'Could not reach the server.',
      });
    }
  };

  const handleSaveServer = () => {
    const nextBase = setApiBase(serverInput);
    setServerInput(nextBase);
    pushToast({ type: 'success', title: 'Saved', message: `Server set to ${nextBase}.` });
  };

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
        <button className="btn btn-ghost" type="button" onClick={() => setConnectionOpen(true)}>
          Connection Settings
        </button>
      </div>
      {connectionOpen && (
        <div style={{ position: 'fixed', inset: 0, display: 'grid', placeItems: 'center', overflow: 'hidden', zIndex: 20 }}>
          <div className="modal-backdrop" onClick={() => setConnectionOpen(false)} />
          <div className="modal-panel glass-surface" onClick={(e) => e.stopPropagation()}>
            <header>
              <div>
                <p className="eyebrow">Connection</p>
                <h3>Server endpoint</h3>
              </div>
              <button className="btn btn-text" onClick={() => setConnectionOpen(false)}>
                Close
              </button>
            </header>
            <label>
              <span>API Base URL</span>
              <input
                className="input dark"
                value={serverInput}
                onChange={(event) => setServerInput(event.target.value)}
                placeholder="http://127.0.0.1:8000"
              />
            </label>
            <footer className="modal-footer">
              <div className="remarks-actions">
                <button className="btn btn-secondary" type="button" onClick={handleTestConnection}>
                  Test Connection
                </button>
                {healthStatus === 'ok' && <span className="muted">Server reachable</span>}
                {healthStatus === 'fail' && <span className="muted">Server unreachable</span>}
              </div>
              <button className="btn btn-primary" type="button" onClick={handleSaveServer}>
                Save
              </button>
            </footer>
          </div>
        </div>
      )}
    </div>
  );
}
