import HeroSection from "@/components/HeroSection";
import MetricsRow from "@/components/MetricsRow";
import NichodCards from "@/components/NichodCards";
import TopicHeatmap from "@/components/TopicHeatmap";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border/50 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <span className="text-xl font-bold text-gradient-brand tracking-tight">RealTalk</span>
          <span className="text-xs font-mono text-muted-foreground">v1.0 — beta</span>
        </div>
      </header>

      <HeroSection />

      <div className="space-y-16 pb-20">
        <MetricsRow />
        <NichodCards />
        <TopicHeatmap />
      </div>

      <footer className="border-t border-border/50 py-8 text-center">
        <p className="text-xs text-muted-foreground">
          Built for creators who listen. <span className="text-gradient-brand font-semibold">RealTalk</span> © 2026
        </p>
      </footer>
    </div>
  );
};

export default Index;
