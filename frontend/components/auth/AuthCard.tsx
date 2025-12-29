import { cn } from "@/lib/utils";

interface AuthCardProps {
  children: React.ReactNode;
  className?: string;
}

export function AuthCard({ children, className }: AuthCardProps) {
  return (
    <div className="w-full min-h-screen flex items-center justify-center p-4">
      <div
        className={cn(
          "w-full max-w-md bg-surface/50 backdrop-blur-lg rounded-2xl border border-border shadow-2xl shadow-primary/10",
          className
        )}
      >
        <div className="p-8 space-y-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gradient">SECURE_TODO</h1>
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
