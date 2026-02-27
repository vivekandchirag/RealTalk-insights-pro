import { motion } from "framer-motion";
import { HelpCircle, Heart, AlertTriangle } from "lucide-react";

interface CommentItem {
  text: string;
  count: number;
}

interface NichodCategory {
  title: string;
  subtitle: string;
  icon: React.ElementType;
  color: string;
  borderColor: string;
  items: CommentItem[];
}

const categories: NichodCategory[] = [
  {
    title: "Questions",
    subtitle: "What the audience is asking",
    icon: HelpCircle,
    color: "text-neon-blue",
    borderColor: "border-neon-blue/30",
    items: [
      { text: "What camera do you use for these shots?", count: 342 },
      { text: "Can you make a tutorial on this setup?", count: 218 },
      { text: "How long did it take to edit this?", count: 156 },
      { text: "What software are you using here?", count: 134 },
      { text: "Will there be a part 2?", count: 97 },
    ],
  },
  {
    title: "Appreciation",
    subtitle: "What's working",
    icon: Heart,
    color: "text-neon-gold",
    borderColor: "border-neon-gold/30",
    items: [
      { text: "Best explanation on YouTube, period.", count: 891 },
      { text: "The editing quality is insane 🔥", count: 654 },
      { text: "This is exactly what I needed today", count: 412 },
      { text: "Your pacing is perfect — never boring", count: 287 },
      { text: "Subscribed after 30 seconds", count: 198 },
    ],
  },
  {
    title: "Criticism",
    subtitle: "Where to improve",
    icon: AlertTriangle,
    color: "text-neon-red",
    borderColor: "border-neon-red/30",
    items: [
      { text: "Audio quality dips around the 5 min mark", count: 76 },
      { text: "The intro is way too long — get to the point", count: 64 },
      { text: "Thumbnail is clickbait, content didn't match", count: 52 },
      { text: "Text on screen is too small to read", count: 41 },
      { text: "Would prefer chapters for navigation", count: 33 },
    ],
  },
];

const NichodCards = () => {
  return (
    <section className="px-4 max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.5 }}
        className="mb-8"
      >
        <h2 className="text-2xl md:text-3xl font-bold text-foreground">
          The <span className="text-gradient-brand">RealTalk</span> Breakdown
        </h2>
        <p className="text-muted-foreground text-sm mt-1">
          Comments categorized by intent — powered by sentiment analysis
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {categories.map((cat, i) => (
          <motion.div
            key={cat.title}
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.4 + i * 0.15, duration: 0.5 }}
            className={`glass-card rounded-xl border-t-2 ${cat.borderColor} overflow-hidden`}
          >
            <div className="p-5 pb-3 flex items-center gap-3">
              <div className={`p-2 rounded-lg bg-muted ${cat.color}`}>
                <cat.icon className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">{cat.title}</h3>
                <p className="text-xs text-muted-foreground">{cat.subtitle}</p>
              </div>
            </div>
            <div className="px-5 pb-5 space-y-3">
              {cat.items.map((item, j) => (
                <div
                  key={j}
                  className="flex items-start justify-between gap-3 py-2 border-b border-border/50 last:border-0"
                >
                  <p className="text-sm text-foreground/80 leading-snug flex-1">
                    "{item.text}"
                  </p>
                  <span className="text-xs font-mono text-muted-foreground whitespace-nowrap mt-0.5">
                    ×{item.count}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};

export default NichodCards;
