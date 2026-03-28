import { AUTOPILOT_THRESHOLD } from '@/lib/constants';
import { getInsightsData } from '@/lib/data';

export default async function InsightsPage() {
  const data = await getInsightsData();
  const week = data.ranges[0];
  const last30 = data.ranges[2];

  return (
    <div className="grid">
      <h2>Insights</h2>
      <section className="grid grid-2">
        {data.ranges.map((range) => (
          <article key={range.days} className="card">
            <h3>Last {range.days} days</h3>
            <p>Average baseline: {range.avgBaseline.toFixed(1)}</p>
            <p>Autopilot crossings: {range.autopilotCrossings}</p>
            <p>Most common trigger: {range.trigger ?? 'No data'}</p>
          </article>
        ))}
      </section>

      <section className="card">
        <h3>Summary</h3>
        <ul>
          <li>
            {data.trend === 'up'
              ? 'Your baseline was higher this week than last week.'
              : data.trend === 'down'
                ? 'Your baseline was lower this week than last week.'
                : 'Your baseline was stable compared to last week.'}
          </li>
          <li>
            {week.trigger
              ? `Most autopilot entries were associated with ${week.trigger.toLowerCase().replaceAll('_', ' ')} triggers.`
              : 'No dominant trigger category appeared this week.'}
          </li>
          <li>
            {last30.avgBaseline < AUTOPILOT_THRESHOLD
              ? 'Your average baseline remained below the autopilot threshold.'
              : 'Your average baseline was at or above the autopilot threshold.'}
          </li>
        </ul>
      </section>
    </div>
  );
}
