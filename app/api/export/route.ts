import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { DEFAULT_USER_ID } from '@/lib/constants';

export async function GET() {
  const [baselines, stress] = await Promise.all([
    prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'asc' } }),
    prisma.stressEvent.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'asc' } })
  ]);

  const lines = [
    'type,timestamp,intensity,title_or_note,trigger_category,entered_autopilot',
    ...baselines.map((entry) =>
      `baseline,${entry.createdAt.toISOString()},${entry.baselineIntensity},"${entry.notes || ''}",,${entry.baselineIntensity >= 7}`
    ),
    ...stress.map((entry) =>
      `stress,${entry.createdAt.toISOString()},${entry.currentIntensity},"${entry.title}",${entry.triggerCategory},${entry.enteredAutopilot}`
    )
  ];

  return new NextResponse(lines.join('\n'), {
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': 'attachment; filename="erg-export.csv"'
    }
  });
}
