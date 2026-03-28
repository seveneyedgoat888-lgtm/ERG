import { HistoryClient } from '@/components/HistoryClient';
import { prisma } from '@/lib/db';
import { DEFAULT_USER_ID } from '@/lib/constants';
import { ensureDefaultUser } from '@/lib/data';

export default async function HistoryPage() {
  await ensureDefaultUser();
  const [baselines, stressEvents] = await Promise.all([
    prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'desc' } }),
    prisma.stressEvent.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'desc' } })
  ]);

  return <HistoryClient initialBaselines={baselines} initialStressEvents={stressEvents} />;
}
