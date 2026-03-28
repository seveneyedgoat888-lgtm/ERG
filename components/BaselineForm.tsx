'use client';

import { useState } from 'react';

type Props = {
  initial?: { id?: string; date?: string | Date; baselineIntensity?: number; notes?: string | null };
  onSaved?: () => void;
};

export function BaselineForm({ initial, onSaved }: Props) {
  const initialDate = initial?.date ? new Date(initial.date).toISOString().slice(0, 10) : new Date().toISOString().slice(0, 10);
  const [date, setDate] = useState(initialDate);
  const [baselineIntensity, setBaselineIntensity] = useState(initial?.baselineIntensity ?? 4);
  const [notes, setNotes] = useState(initial?.notes ?? '');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);

    const method = initial?.id ? 'PUT' : 'POST';
    const endpoint = initial?.id ? `/api/baselines/${initial.id}` : '/api/baselines';

    const res = await fetch(endpoint, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, baselineIntensity, notes })
    });

    if (!res.ok) {
      setError('Could not save baseline entry. Please check your inputs.');
      return;
    }

    setMessage('Baseline saved successfully.');
    onSaved?.();
  };

  return (
    <form className="card grid" onSubmit={handleSubmit}>
      <h2>{initial?.id ? 'Edit baseline entry' : 'Log daily baseline'}</h2>
      <label>
        Date
        <input type="date" required value={date} onChange={(e) => setDate(e.target.value)} />
      </label>
      <label>
        Baseline intensity (1-10)
        <input
          type="number"
          min={1}
          max={10}
          required
          value={baselineIntensity}
          onChange={(e) => setBaselineIntensity(Number(e.target.value))}
        />
      </label>
      <label>
        Notes (optional)
        <textarea rows={3} value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Any context for today?" />
      </label>
      <button type="submit">Save baseline</button>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </form>
  );
}
