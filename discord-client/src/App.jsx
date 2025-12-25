import { useEffect, useState } from 'react';
import { HashRouter, Navigate, Route, Routes } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import ToastStack from './components/ToastStack';
import LoginPage from './pages/LoginPage';
import StudentsPage from './pages/StudentsPage';
import ReportsPage from './pages/ReportsPage';
import DiagnosticsPage from './pages/DiagnosticsPage';
import ResultsPage from './pages/ResultsPage';
import SettingsPage from './pages/SettingsPage';
import useAuthStore from './store/authStore';
import './styles/global.css';

function App() {
  const logout = useAuthStore((state) => state.logout);
  const [updateState, setUpdateState] = useState({ status: 'idle', progress: null, message: '' });

  useEffect(() => {
    const handleBeforeUnload = () => {
      // Clear auth state on window close
      logout();
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [logout]);

  useEffect(() => {
    if (!window?.desktop?.updates?.onStatus) return;
    const unsubscribe = window.desktop.updates.onStatus((payload) => {
      setUpdateState({
        status: payload.status || 'idle',
        progress: payload.progress || null,
        message: payload.message || '',
      });
    });
    return () => unsubscribe?.();
  }, []);

  const handleInstallUpdate = () => {
    window?.desktop?.updates?.install?.();
  };

  return (
    <HashRouter>
      {(updateState.status === 'checking' ||
        updateState.status === 'available' ||
        updateState.status === 'downloading' ||
        updateState.status === 'ready' ||
        updateState.status === 'error') && (
        <div className="update-overlay">
          <div className="update-card glass-surface">
            <p className="eyebrow">Updating</p>
            <h3>
              {updateState.status === 'checking' && 'Checking for updates...'}
              {updateState.status === 'available' && 'Update found. Downloading...'}
              {updateState.status === 'downloading' && 'Downloading update...'}
              {updateState.status === 'ready' && 'Update ready'}
              {updateState.status === 'error' && 'Update error'}
            </h3>
            {updateState.status === 'downloading' && (
              <>
                <div className="update-progress">
                  <div
                    className="update-progress-bar"
                    style={{ width: `${Math.round(updateState.progress?.percent || 0)}%` }}
                  />
                </div>
                <p className="muted">{Math.round(updateState.progress?.percent || 0)}% downloaded</p>
              </>
            )}
            {updateState.status === 'ready' && (
              <button className="btn btn-primary" onClick={handleInstallUpdate}>
                Restart & Update
              </button>
            )}
            {updateState.status === 'error' && (
              <p className="muted">{updateState.message || 'Update failed. Try again later.'}</p>
            )}
          </div>
        </div>
      )}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<MainLayout />}>
          <Route path="/" element={<Navigate to="/students" replace />} />
          <Route path="/students" element={<StudentsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/diagnostics" element={<DiagnosticsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
      </Routes>
      <ToastStack />
    </HashRouter>
  );
}

export default App;
