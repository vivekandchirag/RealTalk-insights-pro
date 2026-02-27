import { motion } from "framer-motion";
import { Flame, Lightbulb } from "lucide-react";

const topics = [
  { keyword: "tutorial", weight: 95, trend: "hot" },
  { keyword: "camera gear", weight: 82, trend: "hot" },
  { keyword: "editing workflow", weight: 78, trend: "rising" },
  { keyword: "behind the scenes", weight: 71, trend: "rising" },
  { keyword: "comparison", weight: 65, trend: "steady" },
  { keyword: "budget setup", weight: 58, trend: "rising" },
  { keyword: "color grading", weight: 54, trend: "steady" },
  { keyword: "lighting tips", weight: 48, trend: "steady" },
  { keyword: "live streaming", weight: 42, trend: "new" },
  { keyword: "shorts vs long", weight: 37, trend: "new" },
];

const getBarColor = (weight: number) => {
  if (weight > 80) return "bg-neon-red";
  if (weight > 60) return "bg-neon-gold";
  return "bg-neon-blue";
};

const getTrendBadge = (trend: string) => {
  const styles: Record<string, string> = {
    hot: "bg-neon-red/15 text-neon-red",
    rising: "bg-neon-gold/15 text-neon-gold",
    steady: "bg-muted text-muted-foreground",
    new: "bg-neon-blue/15 text-neon-blue",
  };
  return styles[trend] || styles.steady;
};

const TopicHeatmap = () => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 1.9, duration: 0.5 }}
      className="px-4 max-w-5xl mx-auto"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-neon-red/10">
          <Lightbulb className="h-5 w-5 text-neon-gold" />
        </div>
        <div>
          <h2 className="text-2xl md:text-3xl font-bold text-foreground">
            Next Video <span className="text-gradient-brand">Ideas</span>
          </h2>
          <p className="text-muted-foreground text-sm">
            Hot topics your audience wants — ranked by demand
          </p>
        </div>
      </div>

      <div className="glass-card rounded-xl p-6 space-y-3">
        {topics.map((topic, i) => (
          <motion.div
            key={topic.keyword}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 2.1 + i * 0.06, duration: 0.4 }}
            className="flex items-center gap-4"
          >
            <span className="text-sm font-medium text-foreground w-36 truncate capitalize">
              {topic.keyword}
            </span>
            <div className="flex-1 h-3 bg-muted rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${topic.weight}%` }}
                transition={{ delay: 2.3 + i * 0.06, duration: 0.6, ease: "easeOut" }}
                className={`h-full rounded-full ${getBarColor(topic.weight)}`}
              />
            </div>
            <span className="text-xs font-mono text-muted-foreground w-10 text-right">
              {topic.weight}%
            </span>
            <span
              className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full ${getTrendBadge(topic.trend)}`}
            >
              {topic.trend === "hot" && <Flame className="inline h-3 w-3 mr-0.5 -mt-0.5" />}
              {topic.trend}
            </span>
          </motion.div>
        ))}
      </div>
    </motion.section>
  );
};

export default TopicHeatmap;
