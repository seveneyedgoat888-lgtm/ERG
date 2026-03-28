export const AUTOPILOT_THRESHOLD = 7;

export const TRIGGER_CATEGORIES = [
  { value: 'RELATIONAL', label: 'Relational' },
  { value: 'WORK_OR_SCHOOL', label: 'Work or school' },
  { value: 'HEALTH', label: 'Health' },
  { value: 'UNCERTAINTY', label: 'Uncertainty' },
  { value: 'OVERSTIMULATION', label: 'Overstimulation' },
  { value: 'MEMORY_TRIGGER', label: 'Memory trigger' },
  { value: 'CONFLICT', label: 'Conflict' },
  { value: 'OTHER', label: 'Other' }
] as const;

export type RangePreset = 'today' | '7d' | '30d' | 'custom';
export const DEFAULT_USER_ID = 'default-user';
