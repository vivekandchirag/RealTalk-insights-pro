import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, Trash2, Clock, ExternalLink, BarChart3 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { getHistory, deleteFromHistory, clearHistory, type HistoryEntry } from "@/lib/history";

const sentimentColor = (label: string) => {
  if (label === "Positive") return "text-[hsl(var(--neon-green))]";
  if (label === "Mixed") return "text-[hsl(var(--neon-gold))]";
  return "text-[hsl(var(--neon-red))]";
};

const History = () => {
  const [entries, setEntries] = useState<HistoryEntry[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    setEntries(getHistory());
  }, []);

  const handleDelete = (id: string) => {
    deleteFromHistory(id);
    setEntries((prev) => prev.filter((e) => e.id !== id));
  };

  const handleClearAll = () => {
    clearHistory();
    setEntries([]);
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border/50 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-gradient-brand tracking-tight">
            RealTalk
          </Link>
          <span className="text-xs font-mono text-muted-foreground">v1.0 — beta</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Page header */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => navigate("/")}
                className="text-muted-foreground hover:text-foreground"
              >
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
                  <Clock className="h-6 w-6 text-[hsl(var(--neon-blue))]" />
                  Analysis History
                </h1>
                <p className="text-sm text-muted-foreground mt-1">
                  {entries.length} {entries.length === 1 ? "analysis" : "analyses"} saved locally
                </p>
              </div>
            </div>
            {entries.length > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleClearAll}
                className="text-[hsl(var(--neon-red))] border-[hsl(var(--neon-red)/0.3)] hover:bg-[hsl(var(--neon-red)/0.1)]"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Clear All
              </Button>
            )}
          </div>

          {/* Empty state */}
          {entries.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col items-center justify-center py-20 text-center"
            >
              <BarChart3 className="h-16 w-16 text-muted-foreground/30 mb-4" />
              <p className="text-lg text-muted-foreground mb-2">No analyses yet</p>
              <p className="text-sm text-muted-foreground/70 mb-6">
                Go back and analyze a YouTube video to see it here.
              </p>
              <Button onClick={() => navigate("/")} className="bg-primary hover:bg-primary/90 text-primary-foreground">
                Analyze a Video
              </Button>
            </motion.div>
          ) : (
            /* History table */
            <div className="glass-card rounded-xl overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow className="border-border/50 hover:bg-transparent">
                    <TableHead className="text-muted-foreground font-semibold">Video URL</TableHead>
                    <TableHead className="text-muted-foreground font-semibold text-center">Comments</TableHead>
                    <TableHead className="text-muted-foreground font-semibold text-center">Sentiment</TableHead>
                    <TableHead className="text-muted-foreground font-semibold text-center">Score</TableHead>
                    <TableHead className="text-muted-foreground font-semibold">Date</TableHead>
                    <TableHead className="text-muted-foreground font-semibold text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <AnimatePresence>
                    {entries.map((entry) => (
                      <motion.tr
                        key={entry.id}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, height: 0 }}
                        className="border-b border-border/50 hover:bg-muted/30 transition-colors"
                      >
                        <TableCell className="max-w-[280px]">
                          <a
                            href={entry.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-[hsl(var(--neon-blue))] hover:underline truncate block flex items-center gap-1.5"
                          >
                            <ExternalLink className="h-3.5 w-3.5 shrink-0" />
                            <span className="truncate">{entry.url}</span>
                          </a>
                        </TableCell>
                        <TableCell className="text-center font-mono text-sm text-foreground">
                          {entry.result.total_comments.toLocaleString()}
                        </TableCell>
                        <TableCell className="text-center">
                          <span className={`text-sm font-medium ${sentimentColor(entry.result.sentiment_label)}`}>
                            {entry.result.sentiment_label}
                          </span>
                        </TableCell>
                        <TableCell className="text-center font-mono text-sm text-foreground">
                          {entry.result.sentiment_score}%
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground whitespace-nowrap">
                          {new Date(entry.analyzedAt).toLocaleDateString("en-US", {
                            month: "short",
                            day: "numeric",
                            year: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </TableCell>
                        <TableCell className="text-right">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDelete(entry.id)}
                            className="h-8 w-8 text-muted-foreground hover:text-[hsl(var(--neon-red))] hover:bg-[hsl(var(--neon-red)/0.1)]"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </TableCell>
                      </motion.tr>
                    ))}
                  </AnimatePresence>
                </TableBody>
              </Table>
            </div>
          )}
        </motion.div>
      </main>

      <footer className="border-t border-border/50 py-8 text-center">
        <p className="text-xs text-muted-foreground">
          Built for creators who listen.{" "}
          <span className="text-gradient-brand font-semibold">RealTalk</span> © 2026
        </p>
      </footer>
    </div>
  );
};

export default History;
