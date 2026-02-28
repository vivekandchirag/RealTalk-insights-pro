import type { AnalyzeResult } from "@/components/HeroSection";

export interface HistoryEntry {
  id: string;
  url: string;
  analyzedAt: string; // ISO string
  result: AnalyzeResult;
}

const STORAGE_KEY = "realtalk_history";

export function getHistory(): HistoryEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveToHistory(url: string, result: AnalyzeResult): void {
  const history = getHistory();
  const entry: HistoryEntry = {
    id: crypto.randomUUID(),
    url,
    analyzedAt: new Date().toISOString(),
    result,
  };
  // Prepend newest first, cap at 50
  history.unshift(entry);
  if (history.length > 50) history.length = 50;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

export function deleteFromHistory(id: string): void {
  const history = getHistory().filter((e) => e.id !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

export function clearHistory(): void {
  localStorage.removeItem(STORAGE_KEY);
}
