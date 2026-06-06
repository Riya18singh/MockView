import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Sparkles, Mail, Lock, User } from "lucide-react";
import { MeshBackground } from "@/components/MeshBackground";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";

export const Route = createFileRoute("/auth")({
  head: () => ({ meta: [{ title: "Sign in — MockView" }] }),
  component: AuthPage,
});

const API = axios.create({ baseURL: "http://localhost:8000/api" });

function AuthPage() {
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    setError("");
    setLoading(true);
    try {
      if (mode === "login") {
        const res = await API.post("/users/login/", { username, password });
        console.log('Django response:', res.data);
        localStorage.setItem("token", res.data.tokens?.access || res.data.access);
        localStorage.setItem("refresh", res.data.tokens?.refresh || res.data.refresh);
        localStorage.setItem("user", JSON.stringify(res.data.user));
        navigate({ to: "/dashboard" });
      } else {
        const res = await API.post("/users/register/", { name, username, password });
        localStorage.setItem("token", res.data.tokens?.access || res.data.access);
        localStorage.setItem("refresh", res.data.tokens?.refresh || res.data.refresh);
        localStorage.setItem("user", JSON.stringify(res.data.user));
        navigate({ to: "/dashboard" });
      }
    } catch (err: any) {
      setError(err.response?.data?.error || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative grid min-h-screen place-items-center px-4">
      <MeshBackground />

      <div className="glass-card w-full max-w-md p-8 animate-scale-in">
        <div className="mb-6 flex rounded-xl bg-secondary p-1">
          {(["login", "signup"] as const).map((m) => (
            <button
              key={m}
              onClick={() => { setMode(m); setError(""); }}
              className={
                "flex-1 rounded-lg px-4 py-2 text-sm font-semibold transition " +
                (mode === m ? "gradient-bg text-white glow" : "text-muted-foreground")
              }
            >
              {m === "login" ? "Login" : "Sign up"}
            </button>
          ))}
        </div>

        <h1 className="text-2xl font-extrabold">
          {mode === "login" ? "Welcome back" : "Create your account"}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {mode === "login" ? "Sign in to continue practicing." : "Start landing offers today."}
        </p>

        {error && (
          <div className="mt-4 rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
            {error}
          </div>
        )}

        <form className="mt-6 space-y-4" onSubmit={(e) => e.preventDefault()}>
          {mode === "signup" && (
            <div>
              <Label htmlFor="name">Full name</Label>
              <div className="relative mt-1.5">
                <User className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="name"
                  placeholder="Ada Lovelace"
                  className="pl-9"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            </div>
          )}

          <div>
            <Label htmlFor="username">Username</Label>
            <div className="relative mt-1.5">
              <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                id="username"
                placeholder="your_username"
                className="pl-9"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
          </div>

          <div>
            <Label htmlFor="password">Password</Label>
            <div className="relative mt-1.5">
              <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                className="pl-9"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <Button
            type="button"
            onClick={handleSubmit}
            disabled={loading}
            className="w-full gradient-bg text-white border-0 glow-hover h-11"
          >
            {loading ? "Please wait..." : mode === "login" ? "Login" : "Create account"}
          </Button>
        </form>

        <div className="my-5 flex items-center gap-3 text-xs text-muted-foreground">
          <div className="h-px flex-1 bg-border" />OR
          <div className="h-px flex-1 bg-border" />
        </div>

        <Button variant="outline" className="w-full h-11 bg-card/40 backdrop-blur">
          <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
            <path fill="#EA4335" d="M12 10.2v3.9h5.5c-.2 1.5-1.7 4.3-5.5 4.3-3.3 0-6-2.7-6-6.1s2.7-6.1 6-6.1c1.9 0 3.1.8 3.8 1.5l2.6-2.5C16.7 3.5 14.6 2.5 12 2.5 6.8 2.5 2.6 6.7 2.6 12s4.2 9.5 9.4 9.5c5.4 0 9-3.8 9-9.2 0-.6-.1-1.1-.2-1.6H12z" />
          </svg>
          Continue with Google
        </Button>
      </div>
    </div>
  );
}