export type CombinedPoint = {
  id: string;
  timestamp: Date;
  intensity: number;
  type: 'baseline' | 'stress';
  label?: string | null;
  triggerCategory?: string;
  enteredAutopilot?: boolean;
};
