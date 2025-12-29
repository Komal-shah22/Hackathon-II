import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        primary:
          "bg-blue-500/20 text-blue-400 border border-blue-500/50",
        accent:
          "bg-cyan-500/20 text-cyan-400 border border-cyan-500/50",
        secondary:
          "bg-gray-500/20 text-gray-400 border border-gray-500/50",
        danger:
          "bg-red-500/20 text-red-400 border border-red-500/50", // Changed to text-primary-text
        outline: "text-gray-400 border border-gray-500/50",
                info:
                  "bg-green-500/20 text-green-400 border border-green-500/50",
                success:
                  "bg-green-500/20 text-green-400 border border-green-500/50",
                warning:
                  "bg-yellow-500/20 text-yellow-400 border border-yellow-500/50",
      },
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
