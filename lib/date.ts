import { endOfDay, startOfDay, subDays } from 'date-fns';
import type { RangePreset } from './constants';

export function rangeFromPreset(preset: RangePreset, customStart?: string, customEnd?: string) {
  const now = new Date();
  if (preset === 'today') {
    return { start: startOfDay(now), end: endOfDay(now) };
  }
  if (preset === '7d') {
    return { start: startOfDay(subDays(now, 6)), end: endOfDay(now) };
  }
  if (preset === '30d') {
    return { start: startOfDay(subDays(now, 29)), end: endOfDay(now) };
  }

  return {
    start: customStart ? startOfDay(new Date(customStart)) : startOfDay(subDays(now, 6)),
    end: customEnd ? endOfDay(new Date(customEnd)) : endOfDay(now)
  };
}
