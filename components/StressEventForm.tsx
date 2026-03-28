'use client';

import { useState } from 'react';
import { TRIGGER_CATEGORIES } from '@/lib/constants';

type StressInitial = {
  id?: string;
  title?: string;
  description?: string | null;
  stressIncrease?: number;
  currentIntensity?: number;
  triggerCategory?: string;
  copingUsed?: string | null;
  enteredAutopilot?: boolean;
};

export function StressEventForm({ initial, onSaved }: { initial?: StressInitial; onSaved?: () => void }) {
  const [title, setTitle] = useState(initial?.title ?? '');
  const [description, setDescription] = useState(initial?.description ?? '');
  const [stressIncrease, setStressIncrease] = useState(initial?.stressIncrease ?? 1);
  const [currentIntensity, setCurrentIntensity] = useState(initial?.currentIntensity ?? 5);
  const [triggerCategory, setTriggerCategory] = useState(initial?.triggerCategory ?? 'RELATIONAL');
  const [copingUsed, setCopingUsed] = useState(initial?.copingUsed ?? '');
  const [enteredAutopilot, setEnteredAutopilot] = useState(initial?.enteredAutopilot ?? false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);

    const method = initial?.id ? 'PUT' : 'POST';
    const endpoint = initial?.id ? `/api/stress-events/${initial.id}` : '/api/stress-events';

    const res = await fetch(endpoint, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        description,
        stressIncrease,
        currentIntensity,
        triggerCategory,
        copingUsed,
        enteredAutopilot
      })
    });

    if (!res.ok) {
      setError('Could not save stress event. Please check your inputs.');
      return;
    }

    setMessage('Stress event saved successfully.');
    if (!initial?.id) {
      setTitle('');
      setDescription('');
      setStressIncrease(1);
      setCurrentIntensity(5);
      setTriggerCategory('RELATIONAL');
      setCopingUsed('');
      setEnteredAutopilot(false);
    }
    onSaved?.();
  };

  return (
    <form className="card grid" onSubmit={handleSubmit}>
      <h2>{initial?.id ? 'Edit stress event' : 'Log stress event'}</h2>
      <label>
        Event title
        <input required value={title} onChange={(e) => setTitle(e.target.value)} maxLength={120} />
      </label>
      <label>
        Description (optional)
        <textarea rows={3} value={description} onChange={(e) => setDescription(e.target.value)} />
      </label>
      <div className="grid grid-2">
        <label>
          Stress increase (1-5)
          <input
            type="number"
            min={1}
            max={5}
            required
            value={stressIncrease}
            onChange={(e) => setStressIncrease(Number(e.target.value))}
          />
        </label>
        <label>
          Current emotional intensity (1-10)
          <input
            type="number"
            min={1}
            max={10}
            required
            value={currentIntensity}
            onChange={(e) => setCurrentIntensity(Number(e.target.value))}
          />
        </label>
      </div>
      <label>
        Trigger category
        <select value={triggerCategory} onChange={(e) => setTriggerCategory(e.target.value)}>
          {TRIGGER_CATEGORIES.map((trigger) => (
            <option key={trigger.value} value={trigger.value}>
              {trigger.label}
            </option>
          ))}
        </select>
      </label>
      <label>
        Coping strategy used (optional)
        <input value={copingUsed} onChange={(e) => setCopingUsed(e.target.value)} maxLength={500} />
      </label>
      <label style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
        <input
          type="checkbox"
          checked={enteredAutopilot}
          onChange={(e) => setEnteredAutopilot(e.target.checked)}
          style={{ width: 'auto' }}
        />
        I feel I entered the autopilot zone.
      </label>
      <button type="submit">Save stress event</button>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </form>
  );
}
