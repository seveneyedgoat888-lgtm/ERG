'use client';

import { useMemo, useState } from 'react';
import type { BaselineEntry, StressEvent } from '@prisma/client';
import { format } from 'date-fns';
import { BaselineForm } from './BaselineForm';
import { StressEventForm } from './StressEventForm';

type Props = {
  initialBaselines: BaselineEntry[];
  initialStressEvents: StressEvent[];
};

export function HistoryClient({ initialBaselines, initialStressEvents }: Props) {
  const [baselines, setBaselines] = useState(initialBaselines);
  const [stressEvents, setStressEvents] = useState(initialStressEvents);
  const [filterType, setFilterType] = useState<'all' | 'baseline' | 'stress'>('all');
  const [editing, setEditing] = useState<{ type: 'baseline' | 'stress'; id: string } | null>(null);

  const merged = useMemo(() => {
    const rows = [
      ...baselines.map((entry) => ({ type: 'baseline' as const, createdAt: entry.createdAt, entry })),
      ...stressEvents.map((entry) => ({ type: 'stress' as const, createdAt: entry.createdAt, entry }))
    ]
      .filter((item) => filterType === 'all' || item.type === filterType)
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
    return rows;
  }, [baselines, stressEvents, filterType]);

  const refresh = async () => {
    const [b, s] = await Promise.all([fetch('/api/baselines').then((r) => r.json()), fetch('/api/stress-events').then((r) => r.json())]);
    setBaselines(b);
    setStressEvents(s);
    setEditing(null);
  };

  const handleDelete = async (type: 'baseline' | 'stress', id: string) => {
    const endpoint = type === 'baseline' ? `/api/baselines/${id}` : `/api/stress-events/${id}`;
    await fetch(endpoint, { method: 'DELETE' });
    await refresh();
  };

  return (
    <div className="grid">
      <div className="card" style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', flexWrap: 'wrap' }}>
        <strong>Filter:</strong>
        <button className="secondary" onClick={() => setFilterType('all')}>All</button>
        <button className="secondary" onClick={() => setFilterType('baseline')}>Baseline</button>
        <button className="secondary" onClick={() => setFilterType('stress')}>Stress event</button>
      </div>

      {editing?.type === 'baseline' && (
        <BaselineForm initial={baselines.find((b) => b.id === editing.id)} onSaved={refresh} />
      )}
      {editing?.type === 'stress' && (
        <StressEventForm initial={stressEvents.find((s) => s.id === editing.id)} onSaved={refresh} />
      )}

      <div className="card" style={{ overflowX: 'auto' }}>
        <h2>Recent entries</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Type</th>
              <th>Details</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {merged.map((row) => (
              <tr key={`${row.type}-${row.entry.id}`}>
                <td>{format(new Date(row.createdAt), 'MMM d, yyyy HH:mm')}</td>
                <td>{row.type === 'baseline' ? 'Baseline' : 'Stress event'}</td>
                <td>
                  {row.type === 'baseline'
                    ? `Intensity ${row.entry.baselineIntensity}${row.entry.notes ? ` • ${row.entry.notes}` : ''}`
                    : `${row.entry.title} • Intensity ${row.entry.currentIntensity}`}
                </td>
                <td style={{ display: 'flex', gap: '0.4rem' }}>
                  <button className="secondary" onClick={() => setEditing({ type: row.type, id: row.entry.id })}>Edit</button>
                  <button onClick={() => handleDelete(row.type, row.entry.id)} style={{ background: '#ef4444' }}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
