import './globals.css';
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Emotional Regulation Graph Tracker',
  description: 'Track baseline emotions, stress events, and autopilot zone crossings.'
};

const navItems = [
  { href: '/', label: 'Dashboard' },
  { href: '/log-baseline', label: 'Log Baseline' },
  { href: '/log-stress-event', label: 'Log Stress Event' },
  { href: '/history', label: 'History' },
  { href: '/insights', label: 'Insights' }
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="container">
          <h1>Emotional Regulation Graph Tracker</h1>
          <p className="small">A simple daily tracker for emotional baseline, stress spikes, and recovery patterns.</p>
          <nav className="nav">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href}>
                {item.label}
              </Link>
            ))}
          </nav>
          {children}
        </main>
      </body>
    </html>
  );
}
