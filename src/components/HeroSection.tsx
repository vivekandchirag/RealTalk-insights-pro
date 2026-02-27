import { useState } from "react";
import { motion } from "framer-motion";
import { Search, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const HeroSection = () => {
  const [url, setUrl] = useState("");

  return (
    <motion.section
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, ease: "easeOut" }}
      className="text-center py-16 px-4"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-4">
          <span className="text-gradient-brand">RealTalk</span>
        </h1>
        <p className="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto mb-2">
          YouTube Comment Intelligence for Creators & Audience
        </p>
        <p className="text-foreground text-sm max-w-lg mx-auto mt-6 mb-10">
          Paste a video URL and uncover what your audience truly thinks — questions, praise, and criticism decoded instantly.
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="flex flex-col sm:flex-row items-center gap-3 max-w-2xl mx-auto"
      >
        <div className="relative flex-1 w-full">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          <Input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://youtube.com/watch?v=..."
            className="pl-12 h-14 bg-muted border-border text-foreground placeholder:text-muted-foreground/50 text-base rounded-xl focus-visible:ring-neon-red/50"
          />
        </div>
        <Button
          size="lg"
          className="h-14 px-8 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold rounded-xl glow-red whitespace-nowrap"
        >
          <Sparkles className="mr-2 h-5 w-5" />
          Generate Insight
        </Button>
      </motion.div>
    </motion.section>
  );
};

export default HeroSection;
