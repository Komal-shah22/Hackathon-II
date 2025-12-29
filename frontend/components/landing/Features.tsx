
import { FiTarget, FiRepeat, FiShield, FiTag, FiCalendar, FiFilter } from 'react-icons/fi';

const features = [
  {
    icon: <FiTarget className="w-8 h-8 text-primary" />,
    title: 'Smart Priorities',
    description: 'High, Medium, Low priorities to focus on what matters.',
  },
  {
    icon: <FiRepeat className="w-8 h-8 text-primary" />,
    title: 'Recurring Tasks',
    description: 'Automate your habits with daily, weekly, or monthly tasks.',
  },
  {
    icon: <FiShield className="w-8 h-8 text-primary" />,
    title: 'Secure & Private',
    description: 'Your data is encrypted. Your privacy is our priority.',
  },
  {
    icon: <FiTag className="w-8 h-8 text-primary" />,
    title: 'Tags & Search',
    description: 'Organize with tags and find any task instantly.',
  },
  {
    icon: <FiCalendar className="w-8 h-8 text-primary" />,
    title: 'Due Dates',
    description: 'Never miss a deadline with smart due date tracking.',
  },
  {
    icon: <FiFilter className="w-8 h-8 text-primary" />,
    title: 'Advanced Filters',
    description: 'Filter your tasks by multiple criteria to find exactly what you need.',
  },
];

export function Features() {
  return (
    <section className="relative py-24 bg-background">
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
        <h2 className="text-3xl md:text-4xl font-semibold text-center mb-12">
          A Feature Set That <span className="text-gradient">Secures</span> Your Productivity
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-surface p-8 rounded-lg border border-border transform hover:-translate-y-2 hover:shadow-glow transition-all duration-300"
            >
              <div className="mb-4">{feature.icon}</div>
              <h3 className="text-xl font-medium mb-2">{feature.title}</h3>
              <p className="text-secondary-text">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
