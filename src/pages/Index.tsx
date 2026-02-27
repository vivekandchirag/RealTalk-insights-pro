import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import HeroSection from "@/components/HeroSection";
import MetricsRow from "@/components/MetricsRow";
import NichodCards from "@/components/NichodCards";
import TopicHeatmap from "@/components/TopicHeatmap";
import type { AnalyzeResult } from "@/components/HeroSection";

const Index = () => {
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border/50 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <span className="text-xl font-bold text-gradient-brand tracking-tight">RealTalk</span>
          <span className="text-xs font-mono text-muted-foreground">v1.0 — beta</span>
        </div>
      </header>

      <HeroSection
        onResult={setResult}
        onLoading={setLoading}
        onError={setError}
      />

      {/* Loading state */}
      <AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="flex flex-col items-center gap-4 py-12 text-muted-foreground"
          >
            <div className="h-10 w-10 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            <p className="text-sm">Fetching &amp; analysing comments…</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error state */}
      <AnimatePresence>
        {error && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="max-w-2xl mx-auto px-4 py-3 mb-6 rounded-xl bg-neon-red/10 border border-neon-red/30 text-neon-red text-sm"
          >
            ⚠️ {error}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results */}
      <AnimatePresence>
        {result && !loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-16 pb-20"
          >
            <MetricsRow
              totalComments={result.total_comments}
              sentimentScore={result.sentiment_score}
              sentimentLabel={result.sentiment_label}
              engagement={result.engagement}
            />
            <NichodCards
              questions={result.questions}
              appreciation={result.appreciation}
              criticism={result.criticism}
            />
            <TopicHeatmap topics={result.topics} />
          </motion.div>
        )}
      </AnimatePresence>

      <footer className="border-t border-border/50 py-8 text-center">
        <p className="text-xs text-muted-foreground">
          Built for creators who listen.{" "}
          <span className="text-gradient-brand font-semibold">RealTalk</span> © 2026
        </p>
      </footer>
    </div>
  );
};

export default Index;
