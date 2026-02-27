import { motion } from "framer-motion";
import { MessageSquare, TrendingUp, Users } from "lucide-react";

const metrics = [
  {
    label: "Total Comments Scanned",
    value: "12,847",
    icon: MessageSquare,
    color: "text-neon-blue",
    glow: "glow-blue",
  },
  {
    label: "Overall Sentiment Score",
    value: "78.4%",
    sublabel: "Positive",
    icon: TrendingUp,
    color: "text-neon-green",
    glow: "",
  },
  {
    label: "Estimated Creator Engagement",
    value: "4.2%",
    icon: Users,
    color: "text-neon-gold",
    glow: "glow-gold",
  },
];

const MetricsRow = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 px-4 max-w-5xl mx-auto">
      {metrics.map((m, i) => (
        <motion.div
          key={m.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 + i * 0.15, duration: 0.5 }}
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
