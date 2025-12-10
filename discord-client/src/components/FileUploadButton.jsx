import { useRef } from 'react';

export default function FileUploadButton({ label, loading, onSelect, accept = '.xlsx,.xls' }) {
  const inputRef = useRef(null);

  const handleClick = () => inputRef.current?.click();
  const handleChange = (event) => {
    const file = event.target.files?.[0];
    if (file && onSelect) {
      onSelect(file);
    }
    event.target.value = '';
  };

  return (
    <>
      <button className="btn btn-secondary" onClick={handleClick} disabled={loading}>
        {loading ? 'Uploading…' : label}
      </button>
      <input type="file" ref={inputRef} className="hidden-input" accept={accept} onChange={handleChange} />
    </>
  );
}
