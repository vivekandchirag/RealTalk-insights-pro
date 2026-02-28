import { motion } from "framer-motion";
import { HelpCircle, Heart, AlertTriangle } from "lucide-react";

interface CommentItem {
  text: string;
  count: number;
}

interface NichodCardsProps {
  questions: CommentItem[];
  appreciation: CommentItem[];
  criticism: CommentItem[];
}

const NichodCards = ({ questions, appreciation, criticism }: NichodCardsProps) => {
  const categories = [
    {
      title: "Questions",
      subtitle: "What the audience is asking",
      icon: HelpCircle,
      color: "text-neon-blue",
      borderColor: "border-neon-blue/30",
      items: questions,
    },
    {
      title: "Appreciation",
      subtitle: "What's working",
      icon: Heart,
      color: "text-neon-gold",
      borderColor: "border-neon-gold/30",
      items: appreciation,
    },
    {
      title: "Criticism",
      subtitle: "Where to improve",
      icon: AlertTriangle,
      color: "text-neon-red",
      borderColor: "border-neon-red/30",
      items: criticism,
    },
  ];

  return (
    <section className="px-4 max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1, duration: 0.5 }}
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
            transition={{ delay: 0.15 + i * 0.15, duration: 0.5 }}
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
              {cat.items.length === 0 ? (
                <p className="text-xs text-muted-foreground italic">No comments in this category.</p>
              ) : (
                cat.items.slice(0, 7).map((item, j) => (
                  <div
                    key={j}
                    className="flex items-start justify-between gap-3 py-2 border-b border-border/50 last:border-0"
                  >
                    <p className="text-sm text-foreground/80 leading-snug flex-1">
                      "{item.text.length > 110 ? item.text.slice(0, 110) + "…" : item.text}"
                    </p>
                    {item.count > 1 && (
                      <span className="text-xs font-mono text-muted-foreground whitespace-nowrap mt-0.5">
                        ×{item.count}
                      </span>
                    )}
                  </div>
                ))
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};

export default NichodCards;
