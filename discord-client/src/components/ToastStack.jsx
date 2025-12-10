import { AnimatePresence, motion } from 'framer-motion';
import useToastStore from '../store/toastStore';

const toastVariants = {
  initial: { opacity: 0, x: 80, scale: 0.95 },
  animate: { opacity: 1, x: 0, scale: 1 },
  exit: { opacity: 0, x: 80, scale: 0.95 },
};

const typeAccent = {
  info: '#5865f2',
  success: '#3ba55d',
  error: '#ed4245',
  warning: '#f0b232',
};

export default function ToastStack() {
  const toasts = useToastStore((state) => state.toasts);
  const dismissToast = useToastStore((state) => state.dismissToast);

  return (
    <div className="toast-stack">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            className="toast-item glass-surface"
            variants={toastVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.2 }}
          >
            <div className="toast-indicator" style={{ backgroundColor: typeAccent[toast.type] }} />
            <div className="toast-body">
              {toast.title && <p className="toast-title">{toast.title}</p>}
              <p className="toast-message">{toast.message}</p>
            </div>
            <button className="toast-close" onClick={() => dismissToast(toast.id)}>
              ×
            </button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
