import Link from 'next/link';
import { Button } from '../ui/button';

export function Hero() {
  return (
    <section className="relative w-full h-screen flex items-center justify-center overflow-hidden">
      {/* Grid Background Overlay */}
      <div
        className="absolute inset-0 z-0 bg-background"
        style={{
          backgroundImage: `
            linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px',
        }}
      />
      {/* Radial Gradient */}
      <div
        className="absolute inset-0 z-0"
        style={{
          background: 'radial-gradient(circle at center, rgba(0,212,255,0.05) 0%, transparent 50%)',
        }}
      />

      <div className="relative z-10 container mx-auto px-4 text-center">
        <div className="mb-4 flex items-center justify-center gap-2 text-sm text-secondary-text">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-success"></span>
          </span>
          SYSTEM ONLINE V3.0
        </div>
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-4">
          MASTER YOUR TASKS
          <br />
          <span className="text-gradient animate-gradient-x bg-[length:200%_auto] bg-clip-text text-transparent from-primary to-accent">
            SECURE.
          </span>
        </h1>
        <p className="max-w-xl mx-auto text-secondary-text mb-8">
          The ultimate todo app for serious productivity. Recurring tasks, priorities, tags, due dates, and powerful filtering—all in one sleek interface.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link href="/signup">
            <Button size="lg">GET STARTED FREE →</Button>
          </Link>
          <Link href="/signin">
            <Button size="lg" variant="outline">
              SIGN IN
            </Button>
          </Link>
        </div>
      </div>
      {/* Placeholder for Task Preview Animation */}
      <div className="absolute bottom-10 right-10 w-72 h-48 bg-surface/50 backdrop-blur-lg rounded-lg border border-border p-4 hidden lg:block animate-fade-in">
        <p className="text-sm font-mono text-muted-text">{'// Task Preview'}</p>
        <div className="mt-2 space-y-2">
            <div className="w-full h-8 bg-surface-light rounded-sm animate-pulse-slow"></div>
            <div className="w-3/4 h-8 bg-surface-light rounded-sm animate-pulse-slow delay-100"></div>
            <div className="w-1/2 h-8 bg-surface-light rounded-sm animate-pulse-slow delay-200"></div>
        </div>
      </div>
    </section>
  );
}
