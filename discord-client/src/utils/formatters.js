export function gradeFromPercentage(value) {
  const pct = Number(value);
  if (Number.isNaN(pct)) return '-';
  if (pct >= 80) return 'A1';
  if (pct >= 70) return 'A';
  if (pct >= 60) return 'B';
  if (pct >= 50) return 'C';
  if (pct >= 40) return 'D';
  return 'U';
}

export function formatPercent(value) {
  if (value === 'Absent') return 'Absent';
  const num = Number(value);
  if (Number.isNaN(num)) return '0%';
  return `${num.toFixed(1)}%`;
}
