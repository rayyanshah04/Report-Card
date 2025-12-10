import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';
import useAuthStore from '../store/authStore';

const getDesktopApi = () => (typeof window !== 'undefined' ? window.desktop : undefined);

export default function TopBar({ title, subtitle }) {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();
  const [isMaximized, setIsMaximized] = useState(false);
  const desktopApi = getDesktopApi();
  const isDesktop = Boolean(desktopApi?.controls);

  useEffect(() => {
    if (!isDesktop || !desktopApi?.onWindowStateChange) return undefined;
    const unsubscribe = desktopApi.onWindowStateChange((state) => {
      setIsMaximized(state === 'maximized');
    });
    desktopApi.controls?.getState?.().then((state) => {
      if (state) {
        setIsMaximized(state === 'maximized');
      }
    });
    return unsubscribe;
  }, [desktopApi, isDesktop]);

  const handleMinimize = () => desktopApi?.controls?.minimize?.();
  const handleMaximize = () => desktopApi?.controls?.maximize?.();
  const handleClose = () => desktopApi?.controls?.close?.();

  return (
    <header className="topbar glass-surface">
      <div className="topbar__info drag-region">
        <p className="eyebrow">Faizan Report Studio</p>
        <h1>{title}</h1>
        <p className="muted">{subtitle}</p>
      </div>
      <div className="topbar__actions no-drag">
        <button className="btn btn-ghost" onClick={() => navigate('/reports')}>
          Launch Report
        </button>
        <button className="btn btn-primary" onClick={() => navigate('/students')}>
          Student HQ
        </button>
        <div className="user-pill">
          <div className={clsx('avatar', 'avatar--accent')}>
            {user?.username?.slice(0, 2)?.toUpperCase() || 'FA'}
          </div>
          <div>
            <strong>{user?.username || 'Guest'}</strong>
            <p className="muted">{user?.role || 'Viewer'}</p>
          </div>
          <button className="btn btn-text" onClick={logout}>
            Logout
          </button>
        </div>
        {isDesktop && (
          <div className="window-controls">
            <button className="window-controls__btn window-controls__btn--min" onClick={handleMinimize} aria-label="Minimize window">
              <span />
            </button>
            <button
              className={`window-controls__btn window-controls__btn--max ${isMaximized ? 'is-restore' : ''}`}
              onClick={handleMaximize}
              aria-label={isMaximized ? 'Restore window' : 'Maximize window'}
            >
              <span />
            </button>
            <button className="window-controls__btn window-controls__btn--close" onClick={handleClose} aria-label="Close window">
              <span />
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
