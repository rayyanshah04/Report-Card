import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';

export default function RemarksModal({ open, remarks, onInsert, onSave, onClose }) {
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [draft, setDraft] = useState('');

  const handleAdd = () => {
    if (!draft.trim()) return;
    onSave([...(remarks || []), draft.trim()]);
    setDraft('');
  };

  const handleDelete = () => {
    if (selectedIndex < 0) return;
    const next = remarks.filter((_, idx) => idx !== selectedIndex);
    onSave(next);
    setSelectedIndex(-1);
  };

  const handleInsert = () => {
    if (selectedIndex < 0) return;
    onInsert(remarks[selectedIndex]);
    onClose();
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div className="modal-backdrop" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
          <motion.div
            className="modal-panel glass-surface"
            initial={{ scale: 0.92, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.92, opacity: 0 }}
          >
            <header>
              <div>
                <p className="eyebrow">Preset Remarks</p>
                <h3>Manage reusable remarks</h3>
              </div>
              <button className="btn btn-text" onClick={onClose}>
                Close
              </button>
            </header>
            <div className="remarks-list scroll-area">
              {(remarks || []).map((remark, index) => (
                <button
                  key={remark + index}
                  className={`remark-item ${selectedIndex === index ? 'is-selected' : ''}`}
                  onClick={() => setSelectedIndex(index)}
                >
                  {remark}
                </button>
              ))}
              {!remarks?.length && <p className="muted">No presets yet.</p>}
            </div>
            <textarea
              className="input dark"
              rows={3}
              placeholder="Type a new remark..."
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
            />
            <footer className="modal-footer">
              <div className="remarks-actions">
                <button className="btn btn-secondary" onClick={handleAdd}>
                  Add
                </button>
                <button className="btn btn-ghost" onClick={handleDelete} disabled={selectedIndex < 0}>
                  Delete
                </button>
              </div>
              <button className="btn btn-primary" onClick={handleInsert} disabled={selectedIndex < 0}>
                Insert Remark
              </button>
            </footer>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
