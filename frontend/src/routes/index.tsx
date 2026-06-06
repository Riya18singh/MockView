import { createFileRoute, Link } from "@tanstack/react-router";
import { Brain, MessageSquare, Trophy, Zap, PlayCircle, ArrowRight, Check, Star, Sparkles } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { MeshBackground } from "@/components/MeshBackground";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "MockView — Land Your Dream Job with AI" },
      { name: "description", content: "Practice interviews with AI, get instant feedback, get hired faster." },
    ],
  }),
  component: Landing,
});

const features = [
  { icon: Brain, title: "AI Interviewer", desc: "Realistic interviews tailored to your role, stack, and seniority." },
  { icon: MessageSquare, title: "Instant Feedback", desc: "Get scored on clarity, depth, and structure after every answer." },
  { icon: Trophy, title: "Track Progress", desc: "Build streaks, climb grades, and see your growth over time." },
  { icon: Zap, title: "10x Faster Prep", desc: "Replace weeks of mock calls with minutes of focused practice." },
];

const steps = [
  { n: "01", title: "Pick a role", desc: "Choose the job, stack, and difficulty in seconds." },
  { n: "02", title: "Interview live", desc: "Chat with our AI interviewer in real time." },
  { n: "03", title: "Get your report", desc: "Score, strengths, weaknesses, and next steps." },
];

const testimonials = [
  { name: "Aanya R.", role: "SWE @ Stripe", quote: "Did 12 mocks. Landed Stripe. The feedback is brutally good." },
  { name: "Marcus J.", role: "PM @ Notion", quote: "Felt like a real loop. The behavioral coaching is unreal." },
  { name: "Léa M.", role: "ML @ Hugging Face", quote: "Better than any prep course. And it's just… there. 24/7." },
];

const plans = [
  { name: "Free", price: "$0", desc: "Try it out", features: ["3 interviews / mo", "Basic feedback", "Core roles"], cta: "Get started" },
  { name: "Pro", price: "$19", desc: "Most popular", features: ["Unlimited interviews", "Deep AI feedback", "All roles & stacks", "Resume parsing"], cta: "Go Pro", highlight: true },
  { name: "Enterprise", price: "Custom", desc: "For teams", features: ["Team analytics", "Custom rubrics", "SSO & SCIM", "Dedicated support"], cta: "Contact sales" },
];

function Landing() {
  return (
    <div className="relative min-h-screen">
      <MeshBackground />
      <Navbar />

      {/* HERO */}
      <section className="relative mx-auto max-w-7xl px-4 pt-20 pb-28 text-center">
        <div className="mx-auto mb-6 inline-flex items-center gap-2 rounded-full border border-border/60 bg-card/40 px-4 py-1.5 text-xs backdrop-blur">
          <Sparkles className="h-3.5 w-3.5 text-primary" />
          <span>Powered by next-gen AI interviewers</span>
        </div>
        <h1 className="mx-auto max-w-4xl text-5xl font-extrabold leading-[1.05] tracking-tight md:text-7xl">
          Land Your Dream Job <br />
          <span className="gradient-text animate-shimmer-bg">with AI</span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl">
          Practice interviews with AI, get instant feedback, get hired faster.
        </p>
        <div className="mt-10 flex flex-wrap items-center justify-center gap-3">
          <Link to="/dashboard">
            <Button size="lg" className="gradient-bg text-white border-0 glow-hover h-12 px-7 text-base">
              Get Started Free <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
          <Button size="lg" variant="outline" className="h-12 px-7 text-base backdrop-blur bg-card/40">
            <PlayCircle className="mr-2 h-4 w-4" /> Watch Demo
          </Button>
        </div>

        {/* preview card */}
        <div className="mx-auto mt-20 max-w-4xl">
          <div className="glass-card overflow-hidden p-2">
            <div className="rounded-xl bg-background/60 p-6 text-left">
              <div className="mb-4 flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-destructive/70" />
                <div className="h-3 w-3 rounded-full bg-warning/70" />
                <div className="h-3 w-3 rounded-full bg-success/70" />
                <span className="ml-3 text-xs text-muted-foreground">MockView · Senior Frontend Loop</span>
              </div>
              <div className="space-y-3 text-sm">
                <div className="flex gap-3">
                  <div className="grid h-8 w-8 shrink-0 place-items-center rounded-full gradient-bg text-white text-xs font-bold">AI</div>
                  <div className="rounded-2xl rounded-tl-sm bg-secondary px-4 py-2.5">Walk me through how you'd design a real-time collaborative editor.</div>
                </div>
                <div className="flex justify-end gap-3">
                  <div className="rounded-2xl rounded-tr-sm gradient-bg px-4 py-2.5 text-white max-w-md">I'd start with operational transforms vs CRDTs, then walk through the sync layer…</div>
                </div>
                <div className="flex gap-3">
                  <div className="grid h-8 w-8 shrink-0 place-items-center rounded-full gradient-bg text-white text-xs font-bold">AI</div>
                  <div className="rounded-2xl rounded-tl-sm bg-secondary px-4 py-2.5 inline-flex gap-1">
                    <span className="h-2 w-2 rounded-full bg-foreground/60 animate-typing-dot" />
                    <span className="h-2 w-2 rounded-full bg-foreground/60 animate-typing-dot" style={{ animationDelay: "0.15s" }} />
                    <span className="h-2 w-2 rounded-full bg-foreground/60 animate-typing-dot" style={{ animationDelay: "0.3s" }} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className="mx-auto max-w-7xl px-4 py-20">
        <div className="mb-12 text-center">
          <h2 className="text-4xl font-extrabold md:text-5xl">Everything you need to <span className="gradient-text">crush it</span></h2>
          <p className="mt-3 text-muted-foreground">Built for the next generation of job seekers.</p>
        </div>
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          {features.map((f) => (
            <div key={f.title} className="glass-card glow-hover p-6">
              <div className="mb-4 inline-grid h-11 w-11 place-items-center rounded-xl gradient-bg glow">
                <f.icon className="h-5 w-5 text-white" />
              </div>
              <h3 className="text-lg font-bold">{f.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how" className="mx-auto max-w-7xl px-4 py-20">
        <div className="mb-12 text-center">
          <h2 className="text-4xl font-extrabold md:text-5xl">How it <span className="gradient-text">works</span></h2>
        </div>
        <div className="grid gap-5 md:grid-cols-3">
          {steps.map((s) => (
            <div key={s.n} className="glass-card p-8">
              <div className="mb-4 text-5xl font-extrabold gradient-text">{s.n}</div>
              <h3 className="text-xl font-bold">{s.title}</h3>
              <p className="mt-2 text-muted-foreground">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className="mx-auto max-w-7xl px-4 py-20">
        <div className="mb-12 text-center">
          <h2 className="text-4xl font-extrabold md:text-5xl">Loved by <span className="gradient-text">10,000+ candidates</span></h2>
        </div>
        <div className="grid gap-5 md:grid-cols-3">
          {testimonials.map((t) => (
            <div key={t.name} className="glass-card p-6">
              <div className="mb-3 flex gap-0.5">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-warning text-warning" />
                ))}
              </div>
              <p className="text-foreground/90">"{t.quote}"</p>
              <div className="mt-5 flex items-center gap-3">
                <div className="grid h-10 w-10 place-items-center rounded-full gradient-bg text-white text-sm font-bold">
                  {t.name[0]}
                </div>
                <div>
                  <div className="text-sm font-semibold">{t.name}</div>
                  <div className="text-xs text-muted-foreground">{t.role}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* PRICING */}
      <section id="pricing" className="mx-auto max-w-7xl px-4 py-20">
        <div className="mb-12 text-center">
          <h2 className="text-4xl font-extrabold md:text-5xl">Simple <span className="gradient-text">pricing</span></h2>
          <p className="mt-3 text-muted-foreground">Start free. Upgrade when you're ready.</p>
        </div>
        <div className="grid gap-5 md:grid-cols-3">
          {plans.map((p) => (
            <div
              key={p.name}
              className={"glass-card p-8 " + (p.highlight ? "glow ring-2 ring-primary/50 md:-translate-y-3" : "")}
            >
              {p.highlight && (
                <div className="mb-3 inline-block rounded-full gradient-bg px-3 py-1 text-xs font-bold text-white">
                  Most popular
                </div>
              )}
              <div className="text-sm text-muted-foreground">{p.desc}</div>
              <div className="mt-1 text-2xl font-bold">{p.name}</div>
              <div className="mt-3 flex items-baseline gap-1">
                <span className="text-5xl font-extrabold">{p.price}</span>
                {p.price.startsWith("$") && p.price !== "$0" && <span className="text-muted-foreground">/mo</span>}
              </div>
              <ul className="my-6 space-y-3 text-sm">
                {p.features.map((f) => (
                  <li key={f} className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-success" /> {f}
                  </li>
                ))}
              </ul>
              <Link to="/auth">
                <Button
                  className={"w-full " + (p.highlight ? "gradient-bg text-white border-0 glow-hover" : "")}
                  variant={p.highlight ? "default" : "outline"}
                >
                  {p.cta}
                </Button>
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-5xl px-4 py-20">
        <div className="glass-card glow p-12 text-center">
          <h2 className="text-4xl font-extrabold md:text-5xl">Your next offer is one mock away.</h2>
          <p className="mt-3 text-muted-foreground">Free forever. No credit card.</p>
          <Link to="/dashboard" className="mt-6 inline-block">
            <Button size="lg" className="gradient-bg text-white border-0 glow-hover h-12 px-7">
              Start practicing <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-border/60 py-10">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-4 text-sm text-muted-foreground md:flex-row">
          <div className="flex items-center gap-2">
            <span className="grid h-7 w-7 place-items-center rounded-lg gradient-bg">
              <Sparkles className="h-3.5 w-3.5 text-white" />
            </span>
            <span className="font-bold text-foreground">MockView</span>
            <span>© {new Date().getFullYear()}</span>
          </div>
          <div className="flex gap-6">
            <a href="#" className="hover:text-foreground">Privacy</a>
            <a href="#" className="hover:text-foreground">Terms</a>
            <a href="#" className="hover:text-foreground">Twitter</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
