import { getDashboardData } from '@/lib/data';
import { prisma } from '@/lib/db';
import { DEFAULT_USER_ID } from '@/lib/constants';
import { DashboardView } from '@/components/DashboardView';

export default async function DashboardPage() {
  const [summary, baselines, stressEvents] = await Promise.all([
    getDashboardData(),
    prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'asc' } }),
    prisma.stressEvent.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'asc' } })
  ]);

  return (
    <div className="grid">
      <section className="grid grid-2">
        <article className="card"><h3>Today&apos;s baseline</h3><p>{summary.todayBaseline?.baselineIntensity ?? 'Not logged yet'}</p></article>
        <article className="card"><h3>Latest emotional intensity</h3><p>{summary.latestIntensity ?? 'No data yet'}</p></article>
        <article className="card"><h3>Stress events this week</h3><p>{summary.stressEventsWeek}</p></article>
        <article className="card"><h3>Autopilot crossings this week</h3><p>{summary.autopilotCrossingsWeek}</p></article>
        <article className="card"><h3>Average baseline this week</h3><p>{summary.averageBaselineWeek.toFixed(1)}</p></article>
        <article className="card"><h3>Most common trigger</h3><p>{summary.commonTriggerWeek ?? 'No stress events'}</p></article>
      </section>
      <div className="card"><a href="/api/export">Export data as CSV</a></div>

      <DashboardView baselines={baselines} stressEvents={stressEvents} />
    </div>
  );
}
