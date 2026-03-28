import { endOfDay, startOfDay, subDays } from 'date-fns';
import { DEFAULT_USER_ID } from './constants';
import { prisma } from './db';
import { averageBaseline, calculateTrendDirection, countThresholdCrossings, mostCommonTriggerCategory } from './analytics';

export async function ensureDefaultUser() {
  return prisma.user.upsert({
    where: { id: DEFAULT_USER_ID },
    update: {},
    create: { id: DEFAULT_USER_ID }
  });
}

export async function getDashboardData() {
  await ensureDefaultUser();
  const now = new Date();
  const startWeek = startOfDay(subDays(now, 6));

  const [todayBaseline, latestStress, weekBaselines, weekStress] = await Promise.all([
    prisma.baselineEntry.findFirst({
      where: { userId: DEFAULT_USER_ID, date: { gte: startOfDay(now), lte: endOfDay(now) } },
      orderBy: { createdAt: 'desc' }
    }),
    prisma.stressEvent.findFirst({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'desc' } }),
    prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID, date: { gte: startWeek, lte: endOfDay(now) } } }),
    prisma.stressEvent.findMany({ where: { userId: DEFAULT_USER_ID, createdAt: { gte: startWeek, lte: endOfDay(now) } } })
  ]);

  const autopilotCrossingsWeek = countThresholdCrossings(weekBaselines, weekStress);
  return {
    todayBaseline,
    latestIntensity: latestStress?.currentIntensity ?? todayBaseline?.baselineIntensity ?? null,
    stressEventsWeek: weekStress.length,
    autopilotCrossingsWeek,
    averageBaselineWeek: averageBaseline(weekBaselines),
    commonTriggerWeek: mostCommonTriggerCategory(weekStress)
  };
}

export async function getInsightsData() {
  await ensureDefaultUser();
  const now = new Date();
  const ranges = [7, 14, 30] as const;

  const results = await Promise.all(
    ranges.map(async (days) => {
      const start = startOfDay(subDays(now, days - 1));
      const [baselines, stress] = await Promise.all([
        prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID, date: { gte: start, lte: endOfDay(now) } } }),
        prisma.stressEvent.findMany({ where: { userId: DEFAULT_USER_ID, createdAt: { gte: start, lte: endOfDay(now) } } })
      ]);
      return {
        days,
        avgBaseline: averageBaseline(baselines),
        autopilotCrossings: countThresholdCrossings(baselines, stress),
        trigger: mostCommonTriggerCategory(stress)
      };
    })
  );

  const currentWeekStart = startOfDay(subDays(now, 6));
  const previousWeekStart = startOfDay(subDays(now, 13));
  const previousWeekEnd = endOfDay(subDays(now, 7));

  const [currentWeek, previousWeek] = await Promise.all([
    prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID, date: { gte: currentWeekStart, lte: endOfDay(now) } } }),
    prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID, date: { gte: previousWeekStart, lte: previousWeekEnd } } })
  ]);

  return {
    ranges: results,
    trend: calculateTrendDirection(averageBaseline(currentWeek), averageBaseline(previousWeek))
  };
}
