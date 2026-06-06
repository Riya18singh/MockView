import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { Send, SkipForward, X, Clock } from "lucide-react";
import { MeshBackground } from "@/components/MeshBackground";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export const Route = createFileRoute("/interview")({
  head: () => ({ meta: [{ title: "Live Interview — MockView" }] }),
  component: Interview,
});

const QUESTIONS = [
  "Tell me about yourself and what drew you to this role.",
  "Walk me through how you'd design a real-time collaborative editor.",
  "Describe a time you disagreed with a teammate. How did you resolve it?",
  "What's the difference between useMemo and useCallback in React?",
  "How would you scale a service to handle 1M requests per second?",
];

type Msg = { from: "ai" | "user"; text: string };

function Interview() {
  const [qIndex, setQIndex] = useState(0);
  const [messages, setMessages] = useState<Msg[]>([{ from: "ai", text: QUESTIONS[0] }]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const t = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, typing]);

  const next = (afterUser?: string) => {
    const ni = qIndex + 1;
    if (afterUser) setMessages((m) => [...m, { from: "user", text: afterUser }]);
    setTyping(true);
    setTimeout(() => {
      setTyping(false);
      if (ni < QUESTIONS.length) {
        setQIndex(ni);
        setMessages((m) => [...m, { from: "ai", text: QUESTIONS[ni] }]);
      } else {
        setMessages((m) => [...m, { from: "ai", text: "Great session — let's wrap up. Generating your report…" }]);
      }
    }, 1200);
  };

  const send = () => {
    if (!input.trim()) return;
    const val = input.trim();
    setInput("");
    next(val);
  };

  const progress = ((qIndex + 1) / QUESTIONS.length) * 100;
  const mm = String(Math.floor(seconds / 60)).padStart(2, "0");
  const ss = String(seconds % 60).padStart(2, "0");

  return (
    <div className="relative flex h-screen flex-col">
      <MeshBackground />

      {/* TOP BAR */}
      <div className="border-b border-border/60 bg-card/40 backdrop-blur-xl">
        <div className="mx-auto max-w-4xl px-4 py-3">
          <div className="flex items-center justify-between gap-4">
            <div className="text-sm font-semibold">
              Question <span className="gradient-text">{Math.min(qIndex + 1, QUESTIONS.length)}</span> / {QUESTIONS.length}
            </div>
            <div className="inline-flex items-center gap-2 text-sm text-muted-foreground">
              <Clock className="h-4 w-4" /> {mm}:{ss}
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" onClick={() => next()}>
                <SkipForward className="mr-1 h-4 w-4" /> Skip
              </Button>
              <Link to="/results">
                <Button variant="destructive" size="sm"><X className="mr-1 h-4 w-4" /> End</Button>
              </Link>
            </div>
          </div>
          <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-secondary">
            <div className="h-full gradient-bg transition-all duration-500" style={{ width: `${progress}%` }} />
          </div>
        </div>
      </div>

      {/* MESSAGES */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-3xl space-y-5 px-4 py-8">
          {messages.map((m, i) => (
            <div key={i} className={"flex gap-3 " + (m.from === "user" ? "justify-end" : "")}>
              {m.from === "ai" && (
                <div className="grid h-9 w-9 shrink-0 place-items-center rounded-full gradient-bg text-white text-xs font-bold glow">AI</div>
              )}
              <div
                className={
                  "max-w-[80%] rounded-2xl px-4 py-3 text-sm animate-fade-in " +
                  (m.from === "ai"
                    ? "rounded-tl-sm glass-card"
                    : "rounded-tr-sm gradient-bg text-white glow")
                }
              >
                {m.text}
              </div>
              {m.from === "user" && (
                <div className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-secondary text-xs font-bold">U</div>
              )}
            </div>
          ))}
          {typing && (
            <div className="flex gap-3">
              <div className="grid h-9 w-9 shrink-0 place-items-center rounded-full gradient-bg text-white text-xs font-bold glow">AI</div>
              <div className="glass-card inline-flex gap-1 rounded-2xl rounded-tl-sm px-4 py-3">
                <span className="h-2 w-2 rounded-full bg-foreground/60 animate-typing-dot" />
                <span className="h-2 w-2 rounded-full bg-foreground/60 animate-typing-dot" style={{ animationDelay: "0.15s" }} />
                <span className="h-2 w-2 rounded-full bg-foreground/60 animate-typing-dot" style={{ animationDelay: "0.3s" }} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* COMPOSER */}
      <div className="border-t border-border/60 bg-card/40 backdrop-blur-xl">
        <div className="mx-auto max-w-3xl px-4 py-4">
          <div className="flex items-center gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Type your answer…"
              className="h-12 bg-background/60"
            />
            <Button onClick={send} className="h-12 px-5 gradient-bg text-white border-0 glow-hover">
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}