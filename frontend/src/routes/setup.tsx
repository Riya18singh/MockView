import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { Upload, X, ArrowRight } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/setup")({
  head: () => ({ meta: [{ title: "New Interview — MockView" }] }),
  component: Setup,
});

const STACKS = ["React", "TypeScript", "Node.js", "Python", "Go", "Rust", "SQL", "AWS", "Kubernetes", "GraphQL", "Next.js", "Tailwind"];

function Setup() {
  const [exp, setExp] = useState("Mid");
  const [type, setType] = useState("Technical");
  const [count, setCount] = useState([5]);
  const [stack, setStack] = useState<string[]>(["React", "TypeScript"]);
  const [dragOver, setDragOver] = useState(false);
  const [file, setFile] = useState<string | null>(null);

  return (
    <AppShell>
      <div className="mx-auto max-w-3xl px-6 py-10 lg:px-10">
        <h1 className="text-3xl font-extrabold md:text-4xl">Configure your <span className="gradient-text">interview</span></h1>
        <p className="mt-1 text-muted-foreground">Tailor it to the role you're targeting.</p>

        <div className="mt-8 space-y-6">
          <Field label="Job role">
            <Select defaultValue="frontend">
              <SelectTrigger className="h-11"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="frontend">Frontend Engineer</SelectItem>
                <SelectItem value="backend">Backend Engineer</SelectItem>
                <SelectItem value="fullstack">Full-stack Engineer</SelectItem>
                <SelectItem value="pm">Product Manager</SelectItem>
                <SelectItem value="data">Data Scientist</SelectItem>
                <SelectItem value="ml">ML Engineer</SelectItem>
              </SelectContent>
            </Select>
          </Field>

          <Field label="Experience">
            <div className="grid grid-cols-3 gap-2">
              {["Fresher", "Mid", "Senior"].map((e) => (
                <button
                  key={e}
                  onClick={() => setExp(e)}
                  className={cn(
                    "rounded-xl border px-4 py-3 text-sm font-semibold transition",
                    exp === e ? "gradient-bg text-white border-transparent glow" : "border-border bg-card/40 hover:bg-secondary"
                  )}
                >
                  {e}
                </button>
              ))}
            </div>
          </Field>

          <Field label="Interview type">
            <div className="grid grid-cols-3 gap-2">
              {["Technical", "HR", "Mixed"].map((t) => (
                <button
                  key={t}
                  onClick={() => setType(t)}
                  className={cn(
                    "rounded-xl border px-4 py-3 text-sm font-semibold transition",
                    type === t ? "gradient-bg text-white border-transparent glow" : "border-border bg-card/40 hover:bg-secondary"
                  )}
                >
                  {t}
                </button>
              ))}
            </div>
          </Field>

          <Field label={`Number of questions: ${count[0]}`}>
            <Slider value={count} onValueChange={setCount} min={3} max={15} step={1} />
          </Field>

          <Field label="Tech stack">
            <div className="flex flex-wrap gap-2">
              {STACKS.map((s) => {
                const active = stack.includes(s);
                return (
                  <button
                    key={s}
                    onClick={() => setStack((p) => (active ? p.filter((x) => x !== s) : [...p, s]))}
                    className={cn(
                      "rounded-full border px-3.5 py-1.5 text-sm transition",
                      active ? "gradient-bg text-white border-transparent glow" : "border-border bg-card/40 hover:bg-secondary"
                    )}
                  >
                    {active && <span className="mr-1">✓</span>}{s}
                  </button>
                );
              })}
            </div>
          </Field>

          <Field label="Resume (optional)">
            <label
              onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragOver(false);
                if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0].name);
              }}
              className={cn(
                "flex cursor-pointer flex-col items-center justify-center gap-2 rounded-2xl border-2 border-dashed p-8 text-center transition",
                dragOver ? "border-primary bg-primary/5" : "border-border bg-card/40"
              )}
            >
              <input
                type="file"
                className="hidden"
                onChange={(e) => e.target.files?.[0] && setFile(e.target.files[0].name)}
              />
              {file ? (
                <div className="inline-flex items-center gap-2 rounded-full bg-secondary px-3 py-1.5 text-sm">
                  {file}
                  <button onClick={(e) => { e.preventDefault(); setFile(null); }}><X className="h-4 w-4" /></button>
                </div>
              ) : (
                <>
                  <Upload className="h-7 w-7 text-muted-foreground" />
                  <div className="text-sm font-medium">Drag & drop your resume</div>
                  <div className="text-xs text-muted-foreground">PDF, DOCX up to 5MB</div>
                </>
              )}
            </label>
          </Field>

          <Link to="/interview" className="block">
            <Button className="w-full h-12 gradient-bg text-white border-0 glow-hover text-base">
              Start Interview <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </div>
    </AppShell>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="glass-card p-5">
      <div className="mb-3 text-sm font-semibold">{label}</div>
      {children}
    </div>
  );
}