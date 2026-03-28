import { describe, expect, it } from 'vitest';
import {
  averageBaseline,
  calculateTrendDirection,
  countThresholdCrossings,
  countStressEvents,
  mostCommonTriggerCategory
} from '@/lib/analytics';

describe('analytics helpers', () => {
  it('calculates average baseline', () => {
    const avg = averageBaseline([
      { baselineIntensity: 4, date: new Date('2026-03-01') },
      { baselineIntensity: 6, date: new Date('2026-03-02') }
    ]);
    expect(avg).toBe(5);
  });

  it('counts stress events', () => {
    expect(
      countStressEvents([
        { currentIntensity: 5, createdAt: new Date() },
        { currentIntensity: 7, createdAt: new Date() }
      ])
    ).toBe(2);
  });

  it('counts threshold crossings for baseline and stress entries', () => {
    const count = countThresholdCrossings(
      [
        { baselineIntensity: 7, date: new Date() },
        { baselineIntensity: 5, date: new Date() }
      ],
      [
        { currentIntensity: 8, createdAt: new Date() },
        { currentIntensity: 6, createdAt: new Date() }
      ]
    );

    expect(count).toBe(2);
  });

  it('calculates trend direction', () => {
    expect(calculateTrendDirection(6, 5)).toBe('up');
    expect(calculateTrendDirection(4, 5)).toBe('down');
    expect(calculateTrendDirection(5.1, 5)).toBe('stable');
  });

  it('finds most common trigger category', () => {
    const trigger = mostCommonTriggerCategory([
      { currentIntensity: 8, createdAt: new Date(), triggerCategory: 'RELATIONAL' },
      { currentIntensity: 7, createdAt: new Date(), triggerCategory: 'CONFLICT' },
      { currentIntensity: 6, createdAt: new Date(), triggerCategory: 'RELATIONAL' }
    ]);
    expect(trigger).toBe('RELATIONAL');
  });
});
