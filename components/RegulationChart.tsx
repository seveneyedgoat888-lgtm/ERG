'use client';

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';
import { format } from 'date-fns';
import { AUTOPILOT_THRESHOLD } from '@/lib/constants';
import type { CombinedPoint } from '@/lib/types';

function normalize(points: CombinedPoint[]) {
  return points.map((point) => ({
    ...point,
    timeLabel: format(new Date(point.timestamp), 'MMM d, HH:mm'),
    baselineIntensity: point.type === 'baseline' ? point.intensity : null,
    stressIntensity: point.type === 'stress' ? point.intensity : null
  }));
}

export function RegulationChart({ points }: { points: CombinedPoint[] }) {
  const data = normalize(points);

  return (
    <div className="card" style={{ height: 360 }}>
      <h2>Emotional regulation graph</h2>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timeLabel" minTickGap={30} />
          <YAxis domain={[1, 10]} allowDecimals={false} />
          <Tooltip
            formatter={(value: number, name) => [value, name === 'baselineIntensity' ? 'Baseline' : 'Stress event']}
            labelFormatter={(label, payload) => {
              const row = payload?.[0]?.payload;
              return `${label} • ${row?.label || 'No note/title'}`;
            }}
          />
          <Legend />
          <ReferenceLine
            y={AUTOPILOT_THRESHOLD}
            stroke="#ef4444"
            strokeDasharray="6 4"
            label={{ value: 'Autopilot Zone (7)', fill: '#ef4444', position: 'insideTopRight' }}
          />
          <Line name="baselineIntensity" type="monotone" dataKey="baselineIntensity" stroke="#2563eb" strokeWidth={2} />
          <Line name="stressIntensity" type="monotone" dataKey="stressIntensity" stroke="#7c3aed" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
