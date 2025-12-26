import { useEffect, useMemo, useState } from 'react';
import StatCard from '../components/StatCard';
import useToast from '../hooks/useToast';
import api from '../services/api';

const termOptions = ['Mid Year', 'Annual Year'];

const toPercent = (value) => `${Number(value || 0).toFixed(1)}%`;

const BarList = ({ title, items, labelKey }) => {
  const maxAvg = Math.max(...items.map((item) => item.avg_pct || 0), 1);
  return (
    <div className="panel glass-surface">
      <header className="panel-header compact">
        <h4>{title}</h4>
      </header>
      <div className="bar-list">
        {items.length ? (
          items.map((item) => (
            <div key={`${labelKey}-${item[labelKey]}`} className="bar-row">
              <div className="bar-label">
                <strong>{item[labelKey]}</strong>
                <span className="muted">{item.count} results</span>
              </div>
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{ width: `${Math.max(6, (item.avg_pct / maxAvg) * 100)}%` }}
                />
              </div>
              <span className="bar-value">{toPercent(item.avg_pct)}</span>
            </div>
          ))
        ) : (
          <p className="muted">No data yet.</p>
        )}
      </div>
    </div>
  );
};

export default function PerformancePage() {
  const toast = useToast();
  const [filters, setFilters] = useState({
    session: 'All',
    classSec: 'All',
    term: 'All',
    search: '',
  });
  const [data, setData] = useState({
    summary: { total_results: 0, avg_pct: 0, grade_counts: {} },
    sessions: [],
    classes: [],
    terms: [],
    timeline: [],
    subjects: [],
    recent: [],
    student_trend: [],
    available: { sessions: [], classes: [], terms: [] },
  });
  const [loading, setLoading] = useState(false);

  const loadAnalytics = async () => {
    const params = {};
    if (filters.session !== 'All') params.session = filters.session;
    if (filters.classSec !== 'All') params.class_sec = filters.classSec;
    if (filters.term !== 'All') params.term = filters.term;
    if (filters.search.trim()) params.search = filters.search.trim();

    setLoading(true);
    try {
      const response = await api.get('/reports/analytics', { params });
      setData(response.data);
    } catch (error) {
      toast({
        type: 'error',
        title: 'Analytics failed',
        message: error.response?.data?.detail || 'Unable to load performance analytics.',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      loadAnalytics();
    }, 200);
    return () => clearTimeout(timeout);
  }, [filters.session, filters.classSec, filters.term, filters.search]);

  const gradeRows = useMemo(() => {
    const entries = Object.entries(data.summary.grade_counts || {});
    return entries.map(([grade, count]) => ({ grade, count })).sort((a, b) => b.count - a.count);
  }, [data.summary.grade_counts]);

  return (
    <div className="performance-page">
      <section className="panel glass-surface">
        <header className="panel-header">
          <div>
            <p className="eyebrow">Performance Radar</p>
            <h3>Every class. Every term. Every trend.</h3>
          </div>
          <button className="btn btn-secondary" onClick={loadAnalytics} disabled={loading}>
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
        </header>
        <div className="filter-bar wide">
          <input
            className="input dark"
            placeholder="Search by student name or G.R No"
            value={filters.search}
            onChange={(event) => setFilters((prev) => ({ ...prev, search: event.target.value }))}
          />
          <select
            className="input dark"
            value={filters.session}
            onChange={(event) => setFilters((prev) => ({ ...prev, session: event.target.value }))}
          >
            <option value="All">All Sessions</option>
            {(data.available.sessions.length ? data.available.sessions : []).map((session) => (
              <option key={session} value={session}>
                {session}
              </option>
            ))}
          </select>
          <select
            className="input dark"
            value={filters.classSec}
            onChange={(event) => setFilters((prev) => ({ ...prev, classSec: event.target.value }))}
          >
            <option value="All">All Classes</option>
            {(data.available.classes.length ? data.available.classes : []).map((cls) => (
              <option key={cls} value={cls}>
                {cls}
              </option>
            ))}
          </select>
          <select
            className="input dark"
            value={filters.term}
            onChange={(event) => setFilters((prev) => ({ ...prev, term: event.target.value }))}
          >
            <option value="All">All Terms</option>
            {(data.available.terms.length ? data.available.terms : termOptions).map((term) => (
              <option key={term} value={term}>
                {term}
              </option>
            ))}
          </select>
          <button className="btn btn-ghost" onClick={() => setFilters({ session: 'All', classSec: 'All', term: 'All', search: '' })}>
            Reset Filters
          </button>
        </div>
        <div className="stat-grid">
          <StatCard label="Total Results" value={data.summary.total_results} accent="iris" />
          <StatCard label="Average %" value={toPercent(data.summary.avg_pct)} accent="emerald" />
          <StatCard label="Active Grades" value={gradeRows.length} accent="sunset" />
        </div>
      </section>

      <section className="performance-grid">
        <BarList title="Session Performance" items={data.sessions} labelKey="session" />
        <BarList title="Class Performance" items={data.classes} labelKey="class_sec" />
        <BarList title="Term Performance" items={data.terms} labelKey="term" />
        <BarList title="Subject Averages" items={data.subjects} labelKey="subject" />
      </section>

      <section className="panel glass-surface">
        <header className="panel-header compact">
          <h4>Grade Distribution</h4>
        </header>
        <div className="grade-grid">
          {gradeRows.length ? (
            gradeRows.map((row) => (
              <div key={row.grade} className="grade-card glass-surface">
                <strong>{row.grade}</strong>
                <span className="muted">{row.count} students</span>
              </div>
            ))
          ) : (
            <p className="muted">No grades recorded yet.</p>
          )}
        </div>
      </section>

      <section className="panel glass-surface">
        <header className="panel-header compact">
          <h4>Recent Results</h4>
        </header>
        {data.recent.length ? (
          <div className="results-table">
            {data.recent.map((row) => (
              <div key={row.id} className="results-row">
                <div>
                  <strong>{row.student_name}</strong>
                  <p className="muted">
                    {row.class_sec} · {row.session} · {row.term}
                  </p>
                </div>
                <div className="results-metrics">
                  <span className="pill">{toPercent(row.pct)}</span>
                  <span className="pill ghost">{row.grade}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="muted">No results found for the current filters.</p>
        )}
      </section>

      {filters.search.trim() && (
        <section className="panel glass-surface">
          <header className="panel-header compact">
            <h4>Student Trend</h4>
          </header>
          {data.student_trend?.length ? (
            <div className="results-table">
              {data.student_trend.map((row, index) => (
                <div key={`${row.session}-${row.term}-${index}`} className="results-row">
                  <div>
                    <strong>{row.session}</strong>
                    <p className="muted">{row.term}</p>
                  </div>
                  <div className="results-metrics">
                    <span className="pill">{toPercent(row.pct)}</span>
                    <span className="pill ghost">{row.grade}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">No trend data for this student yet.</p>
          )}
        </section>
      )}
    </div>
  );
}
