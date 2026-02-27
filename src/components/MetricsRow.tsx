import { motion } from "framer-motion";
import { MessageSquare, TrendingUp, Users } from "lucide-react";

interface MetricsRowProps {
  totalComments: number;
  sentimentScore: number;
  sentimentLabel: string;
  engagement: string;
}

const MetricsRow = ({ totalComments, sentimentScore, sentimentLabel, engagement }: MetricsRowProps) => {
  const metrics = [
    {
      label: "Total Comments Scanned",
      value: totalComments.toLocaleString(),
      icon: MessageSquare,
      color: "text-neon-blue",
      glow: "glow-blue",
    },
    {
      label: "Overall Sentiment Score",
      value: `${sentimentScore}%`,
      sublabel: sentimentLabel,
      icon: TrendingUp,
      color: "text-neon-green",
      glow: "",
    },
    {
      label: "Estimated Creator Engagement",
      value: engagement,
      icon: Users,
      color: "text-neon-gold",
      glow: "glow-gold",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 px-4 max-w-5xl mx-auto">
      {metrics.map((m, i) => (
        <motion.div
          key={m.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 + i * 0.15, duration: 0.5 }}
          className={`glass-card rounded-xl p-6 ${m.glow}`}
        >
          <div className="flex items-center gap-3 mb-3">
            <m.icon className={`h-5 w-5 ${m.color}`} />
            <span className="text-muted-foreground text-sm font-medium">{m.label}</span>
          </div>
          <p className="text-3xl font-bold text-foreground">
            {m.value}
            {m.sublabel && (
              <span className="text-sm font-medium text-neon-green ml-2">{m.sublabel}</span>
            )}
          </p>
        </motion.div>
      ))}
    </div>
  );
};

export default MetricsRow;
