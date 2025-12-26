import { useEffect, useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';

const statusColors = {
  new: 'emerald',
  update: 'iris',
  conflict: 'sunset',
  skip: 'slate',
  error: 'rose',
};

const StatusPill = ({ status }) => (
  <span className={`status-pill status-${statusColors[status] || 'slate'}`}>{status}</span>
);

export default function ImportPreviewModal({ open, preview, onConfirm, onClose }) {
  const [decisions, setDecisions] = useState({});

  useEffect(() => {
    if (!open || !preview?.rows) return;
    const next = {};
    preview.rows.forEach((row) => {
      let action = 'skip';
      if (row.status === 'new') action = 'insert';
      if (row.status === 'update') action = 'update';
      if (row.status === 'conflict') action = 'update';
      next[row.gr_no] = {
        action,
        nameChoice: row.name_conflict ? 'excel' : 'excel',
      };
    });
    setDecisions(next);
  }, [open, preview]);

  const rows = preview?.rows || [];
  const summary = preview?.summary || {};

  const handleDecision = (grNo, updates) => {
    setDecisions((prev) => ({
      ...prev,
      [grNo]: { ...prev[grNo], ...updates },
    }));
  };

  const handleConfirm = () => {
    const payload = Object.entries(decisions).map(([gr_no, values]) => ({ gr_no, ...values }));
    onConfirm(payload);
  };

  const bulkSet = (action) => {
    const next = { ...decisions };
    rows.forEach((row) => {
      if (!row.gr_no || row.status === 'error') return;
      next[row.gr_no] = { ...next[row.gr_no], action };
    });
    setDecisions(next);
  };

  const diffLines = useMemo(
    () =>
      rows.map((row) => {
        if (!row.diffs || !Object.keys(row.diffs).length) return [];
        return Object.entries(row.diffs).map(([field, diff]) => ({
          field,
          db: diff.db ?? '--',
          excel: diff.excel ?? '--',
        }));
      }),
    [rows],
  );

  return (
    <AnimatePresence>
      {open && (
        <div className="modal-root">
          <motion.div className="modal-backdrop" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} />
          <motion.div
            className="modal-panel glass-surface import-preview"
            initial={{ scale: 0.94, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.94, opacity: 0 }}
            onClick={(event) => event.stopPropagation()}
          >
            <header>
              <div>
                <p className="eyebrow">Excel Import Review</p>
                <h3>Confirm changes before writing to the database</h3>
              </div>
              <button className="btn btn-text" onClick={onClose}>
                Close
              </button>
            </header>
            <div className="import-summary">
              <span>Total: {summary.total || 0}</span>
              <span>New: {summary.new || 0}</span>
              <span>Updates: {summary.update || 0}</span>
              <span>Conflicts: {summary.conflict || 0}</span>
              <span>Skip: {summary.skip || 0}</span>
              <span>Errors: {summary.error || 0}</span>
            </div>
            <div className="import-actions">
              <button className="btn btn-secondary" onClick={() => bulkSet('update')}>
                Set All to Update
              </button>
              <button className="btn btn-ghost" onClick={() => bulkSet('skip')}>
                Set All to Skip
              </button>
            </div>
            <div className="import-table scroll-area">
              {rows.length ? (
                rows.map((row, idx) => (
                  <div key={`${row.gr_no}-${row.rowIndex}`} className="import-row">
                    <div className="import-row-main">
                      <div>
                        <strong>{row.excel?.student_name || row.db?.student_name || 'Unknown'}</strong>
                        <p className="muted">G.R No: {row.gr_no || 'Missing'}</p>
                      </div>
                      <StatusPill status={row.status} />
                    </div>
                    {row.error && <p className="muted error-text">{row.error}</p>}
                    {row.status !== 'error' && row.gr_no && (
                      <div className="import-controls">
                        <label>
                          <span>Action</span>
                          <select
                            className="input dark"
                            value={decisions[row.gr_no]?.action || 'skip'}
                            onChange={(event) => handleDecision(row.gr_no, { action: event.target.value })}
                          >
                            <option value="insert">Insert</option>
                            <option value="update">Update</option>
                            <option value="skip">Skip</option>
                          </select>
                        </label>
                        {row.name_conflict && (
                          <label>
                            <span>Name conflict</span>
                            <div className="choice-row">
                              <button
                                className={`btn btn-secondary${decisions[row.gr_no]?.nameChoice === 'excel' ? ' is-active' : ''}`}
                                onClick={() => handleDecision(row.gr_no, { nameChoice: 'excel' })}
                              >
                                Keep Excel
                              </button>
                              <button
                                className={`btn btn-secondary${decisions[row.gr_no]?.nameChoice === 'db' ? ' is-active' : ''}`}
                                onClick={() => handleDecision(row.gr_no, { nameChoice: 'db' })}
                              >
                                Keep Database
                              </button>
                            </div>
                          </label>
                        )}
                      </div>
                    )}
                    {!!diffLines[idx]?.length && (
                      <div className="diff-list">
                        {diffLines[idx].map((diff) => (
                          <div key={`${row.gr_no}-${diff.field}`} className="diff-row">
                            <span>{diff.field}</span>
                            <span className="muted">{diff.db}</span>
                            <span className="diff-arrow">→</span>
                            <span>{diff.excel}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <p className="muted">No rows found in the file.</p>
              )}
            </div>
            <footer className="modal-footer">
              <button className="btn btn-ghost" onClick={onClose}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleConfirm}>
                Confirm Import
              </button>
            </footer>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
