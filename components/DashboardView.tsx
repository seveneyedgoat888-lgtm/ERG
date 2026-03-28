'use client';

import { useMemo, useState } from 'react';
import { format } from 'date-fns';
import type { BaselineEntry, StressEvent } from '@prisma/client';
import { rangeFromPreset } from '@/lib/date';
import type { RangePreset } from '@/lib/constants';
import { RegulationChart } from './RegulationChart';

type Props = {
  baselines: BaselineEntry[];
  stressEvents: StressEvent[];
};

export function DashboardView({ baselines, stressEvents }: Props) {
  const [preset, setPreset] = useState<RangePreset>('7d');
  const [customStart, setCustomStart] = useState('');
  const [customEnd, setCustomEnd] = useState('');

  const combined = useMemo(() => {
    const { start, end } = rangeFromPreset(preset, customStart, customEnd);

    return [
      ...baselines
        .filter((entry) => {
          const time = new Date(entry.createdAt).getTime();
          return time >= start.getTime() && time <= end.getTime();
        })
        .map((entry) => ({
          id: `b-${entry.id}`,
          timestamp: new Date(entry.createdAt),
          intensity: entry.baselineIntensity,
          type: 'baseline' as const,
          label: entry.notes
        })),
      ...stressEvents
        .filter((entry) => {
          const time = new Date(entry.createdAt).getTime();
          return time >= start.getTime() && time <= end.getTime();
        })
        .map((entry) => ({
          id: `s-${entry.id}`,
          timestamp: new Date(entry.createdAt),
          intensity: entry.currentIntensity,
          type: 'stress' as const,
          label: entry.title,
          triggerCategory: entry.triggerCategory,
          enteredAutopilot: entry.enteredAutopilot
        }))
    ].sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
  }, [baselines, stressEvents, preset, customStart, customEnd]);

  return (
    <div className="grid">
      <div className="card grid grid-2">
        <label>
          Filter range
          <select value={preset} onChange={(e) => setPreset(e.target.value as RangePreset)}>
            <option value="today">Today</option>
            <option value="7d">Past 7 days</option>
            <option value="30d">Past 30 days</option>
            <option value="custom">Custom range</option>
          </select>
        </label>
        {preset === 'custom' && (
          <>
            <label>
              Start date
              <input type="date" value={customStart} onChange={(e) => setCustomStart(e.target.value)} />
            </label>
            <label>
              End date
              <input type="date" value={customEnd} onChange={(e) => setCustomEnd(e.target.value)} />
            </label>
          </>
        )}
      </div>
      <RegulationChart points={combined} />
      <div className="card">
        <h3>Plotted entries</h3>
        <p className="small">
          Showing {combined.length} entries from {combined[0] ? format(combined[0].timestamp, 'MMM d, yyyy') : '-'} to{' '}
          {combined.at(-1) ? format(combined.at(-1)!.timestamp, 'MMM d, yyyy') : '-'}.
        </p>
      </div>
    </div>
  );
}
