import Link from 'next/link';
import { Button } from '../ui/button';

export function CTA() {
  return (
    <section className="py-24 bg-background">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Ready to <span className="text-gradient">Secure</span> Your Productivity?
        </h2>
        <p className="text-secondary-text max-w-2xl mx-auto mb-8">
          Stop managing tasks and start mastering them. Get started with Secure Todo for free and experience a new level of productivity.
        </p>
        <Link href="/signup">
          <Button size="lg">
            Create Your Free Account →
          </Button>
        </Link>
      </div>
    </section>
  );
}
