
const steps = [
  {
    step: '01',
    title: 'CREATE',
    subtitle: 'Create Tasks Instantly',
    description: 'Add titles, descriptions, priorities, and tags instantly. Use keyboard shortcuts for maximum speed.',
  },
  {
    step: '02',
    title: 'ORGANIZE',
    subtitle: 'Organize with Smart Features',
    description: 'Filter, sort, and categorize effortlessly. Let the system work for you.',
  },
  {
    step: '03',
    title: 'COMPLETE',
    subtitle: 'Track & Complete',
    description: 'Mark tasks as complete, view your progress, and stay productive.',
  },
];

export function HowItWorks() {
  return (
    <section className="relative py-24 bg-background ">
      {/* Grid Background Overlay */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: `
            linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px',
        }}
      />
      <div className="container mx-auto px-4 relative z-10">
        <h2 className="text-3xl md:text-4xl font-semibold text-center mb-16">
          HOW IT WORKS
        </h2>
        <div className="relative">
          {/* Connecting Line */}
          <div className="absolute left-1/2 -translate-x-1/2 md:left-1/2 md:-translate-x-1/2 top-0 h-full w-px bg-border" />

          {steps.map((item, index) => (
            <div key={index} className="relative flex items-center mb-16">
              <div className="hidden md:flex w-1/2">
                {index % 2 === 0 ? <div className="w-full"></div> : <StepContent {...item} rightAlign={true} />}
              </div>

              <div className="hidden md:flex w-12 h-12 bg-surface border-2 border-primary rounded-full items-center justify-center text-primary font-bold z-10 mx-auto">
                {item.step}
              </div>

              <div className="w-full md:w-1/2 md:pl-8">
                <StepContent {...item} rightAlign={false} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

const StepContent = ({ step, title, subtitle, description, rightAlign }: any) => (
  <div className={`p-6 rounded-lg bg-surface-light border border-border ${rightAlign ? 'md:text-right' : ''}`}>
    <p className="text-sm font-mono text-primary mb-2">{`// ${step} // ${title}`}</p>
    <h3 className="text-2xl font-medium mb-2">{subtitle}</h3>
    <p className="text-secondary-text">{description}</p>
  </div>
);
