import { z } from 'zod';

export const baselineSchema = z.object({
  date: z.string().min(1),
  baselineIntensity: z.coerce.number().int().min(1).max(10),
  notes: z.string().max(1000).optional().or(z.literal(''))
});

export const stressSchema = z.object({
  title: z.string().min(1).max(120),
  description: z.string().max(2000).optional().or(z.literal('')),
  stressIncrease: z.coerce.number().int().min(1).max(5),
  currentIntensity: z.coerce.number().int().min(1).max(10),
  triggerCategory: z.enum([
    'RELATIONAL',
    'WORK_OR_SCHOOL',
    'HEALTH',
    'UNCERTAINTY',
    'OVERSTIMULATION',
    'MEMORY_TRIGGER',
    'CONFLICT',
    'OTHER'
  ]),
  copingUsed: z.string().max(500).optional().or(z.literal('')),
  enteredAutopilot: z.coerce.boolean()
});
