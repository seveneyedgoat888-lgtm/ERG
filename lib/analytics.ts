import { AUTOPILOT_THRESHOLD } from './constants';

export type BaselineSample = { baselineIntensity: number; date: Date };
export type StressSample = { currentIntensity: number; createdAt: Date; triggerCategory?: string | null };

export function averageBaseline(entries: BaselineSample[]) {
  if (!entries.length) return 0;
  return entries.reduce((sum, entry) => sum + entry.baselineIntensity, 0) / entries.length;
}

export function countStressEvents(entries: StressSample[]) {
  return entries.length;
}

export function countThresholdCrossings(
  baselines: BaselineSample[],
  stressEvents: StressSample[],
  threshold = AUTOPILOT_THRESHOLD
) {
  const baselineCrosses = baselines.filter((entry) => entry.baselineIntensity >= threshold).length;
  const stressCrosses = stressEvents.filter((entry) => entry.currentIntensity >= threshold).length;
  return baselineCrosses + stressCrosses;
}

export function calculateTrendDirection(
  recentAverage: number,
  priorAverage: number,
  meaningfulDelta = 0.4
): 'up' | 'down' | 'stable' {
  const delta = recentAverage - priorAverage;
  if (delta > meaningfulDelta) return 'up';
  if (delta < -meaningfulDelta) return 'down';
  return 'stable';
}

export function mostCommonTriggerCategory(stressEvents: StressSample[]) {
  if (!stressEvents.length) return null;

  const counts = stressEvents.reduce<Record<string, number>>((acc, event) => {
    const key = event.triggerCategory || 'UNKNOWN';
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
}
