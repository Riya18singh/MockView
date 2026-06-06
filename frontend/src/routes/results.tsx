import { createFileRoute, Link } from "@tanstack/react-router";
import { Download, RefreshCw, Check, X, ThumbsUp, AlertTriangle } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/results")({
  head: () => ({ meta: [{ title: "Results — MockView" }] }),
  component: Results,
});

const score = 87;
const grade = "A";
const breakdown = [
  { label: "Technical", value: 91 },
  { label: "Communication", value: 84 },
  { label: "Problem Solving", value: 86 },
];
const qa = [
  {
    q: "Walk me through how you'd design a real-time collaborative editor.",
    a: "I'd start with operational transforms vs CRDTs, then walk through the sync layer with websockets...",
    feedback: "Strong structure. Great mention of CRDT trade-offs. Could expand on conflict resolution under network partitions.",
  },
  {
    q: "What's the difference between useMemo and useCallback?",
    a: "useMemo memoizes a value, useCallback memoizes a function reference...",
    feedback: "Accurate and concise. Add a concrete example to make it stand out.",
  },
];
const strengths = ["Clear communication", "Strong fundamentals in React", "Confident pacing"];
const weaknesses = ["System design depth", "Concrete examples", "Edge case coverage"];

function Results() {
  const radius = 90;
  const c = 2 * Math.PI * radius;
  const offset = c - (score / 100) * c;

  return (
    <AppShell>
      <div className="mx-auto max-w-5xl space-y-6 px-6 py-10 lg:px-10">
        <div>
          <h1 className="text-3xl font-extrabold md:text-4xl">Your <span className="gradient-text">results</span></h1>
          <p className="mt-1 text-muted-foreground">Frontend Engineer · Technical · 5 questions</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          <div className="glass-card glow flex flex-col items-center justify-center p-8 text-center">
            <div className="relative">
              <svg width="220" height="220" viewBox="0 0 220 220">
                <defs>
                  <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor="oklch(0.7 0.24 295)" />
                    <stop offset="100%" stopColor="oklch(0.7 0.22 240)" />
                  </linearGradient>
                </defs>
                <circle cx="110" cy="110" r={radius} stroke="var(--secondary)" strokeWidth="14" fill="none" />
                <circle
                  cx="110" cy="110" r={radius}
                  stroke="url(#ring)" strokeWidth="14" fill="none" strokeLinecap="round"
                  strokeDasharray={c} strokeDashoffset={offset}
                  transform="rotate(-90 110 110)"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <div className="text-5xl font-extrabold">{score}</div>
                <div className="text-sm text-muted-foreground">out of 100</div>
              </div>
            </div>
            <div className="mt-4 inline-block rounded-full gradient-bg px-4 py-1 text-sm font-bold text-white">Grade {grade}</div>
          </div>

          <div className="grid gap-4 lg:col-span-2 sm:grid-cols-3">
            {breakdown.map((b) => (
              <div key={b.label} className="glass-card p-5">
                <div className="text-sm text-muted-foreground">{b.label}</div>
                <div className="mt-2 text-3xl font-extrabold">{b.value}</div>
                <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-secondary">
                  <div className="h-full gradient-bg" style={{ width: `${b.value}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <div className="glass-card p-6">
            <h3 className="mb-3 inline-flex items-center gap-2 font-bold">
              <ThumbsUp className="h-4 w-4 text-success" /> Strengths
            </h3>
            <ul className="space-y-2 text-sm">
              {strengths.map((s) => (
                <li key={s} className="flex items-center gap-2 rounded-lg bg-success/10 px-3 py-2 text-success">
                  <Check className="h-4 w-4" /> {s}
                </li>
              ))}
            </ul>
          </div>
          <div className="glass-card p-6">
            <h3 className="mb-3 inline-flex items-center gap-2 font-bold">
              <AlertTriangle className="h-4 w-4 text-destructive" /> Areas to improve
            </h3>
            <ul className="space-y-2 text-sm">
              {weaknesses.map((s) => (
                <li key={s} className="flex items-center gap-2 rounded-lg bg-destructive/10 px-3 py-2 text-destructive">
                  <X className="h-4 w-4" /> {s}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="glass-card p-6">
          <h3 className="mb-4 font-bold">Question-by-question feedback</h3>
          <div className="space-y-4">
            {qa.map((item, i) => (
              <div key={i} className="rounded-2xl border border-border/60 bg-background/40 p-5">
                <div className="text-xs font-semibold uppercase tracking-wider text-primary">Question {i + 1}</div>
                <div className="mt-1 font-semibold">{item.q}</div>
                <div className="mt-3 rounded-xl bg-secondary p-3 text-sm">
                  <div className="text-xs text-muted-foreground mb-1">Your answer</div>
                  {item.a}
                </div>
                <div className="mt-3 rounded-xl gradient-bg p-3 text-sm text-white">
                  <div className="text-xs opacity-80 mb-1">AI feedback</div>
                  {item.feedback}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <Link to="/setup">
            <Button className="gradient-bg text-white border-0 glow-hover h-11">
              <RefreshCw className="mr-2 h-4 w-4" /> Retake
            </Button>
          </Link>
          <Button variant="outline" className="h-11 bg-card/40">
            <Download className="mr-2 h-4 w-4" /> Download Report
          </Button>
        </div>
      </div>
    </AppShell>
  );
}