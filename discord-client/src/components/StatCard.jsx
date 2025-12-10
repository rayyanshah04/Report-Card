import { motion } from 'framer-motion';

export default function StatCard({ label, value, accent = 'indigo', blur = false }) {
  return (
    <motion.div
      className={`stat-card glass-surface accent-${accent} ${blur ? 'is-blur' : ''}`}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
    >
      <p className="stat-label">{label}</p>
      <p className="stat-value">{value}</p>
    </motion.div>
  );
}
