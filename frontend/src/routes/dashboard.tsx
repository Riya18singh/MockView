import { createFileRoute, Link } from "@tanstack/react-router";
import { LineChart, Line, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { Flame, TrendingUp, Award, MessagesSquare, Plus, ArrowUpRight } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import axios from "axios";

export const Route = createFileRoute("/dashboard")({
  head: () => ({ meta: [{ title: "Dashboard — MockView" }] }),
  component: Dashboard,
});

const API = axios.create({ baseURL: "http://localhost:8000/api" });
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) req.headers.Authorization = `Bearer ${token}`;
  return req;
});

function Dashboard() {
  const [stats, setStats] = useState([
    { label: "Total Interviews", value: "...", icon: MessagesSquare, change: "" },
    { label: "Average Score", value: "...", icon: Award, change: "" },
    { label: "Current Streak", value: "...", icon: Flame, change: "" },
    { label: "Improvement", value: "...", icon: TrendingUp, change: "" },
  ]);
  const [chartData, setChartData] = useState([]);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        // Fetch stats
        const statsRes = await API.get("/users/progress/");
        const data = statsRes.data;

        setStats([
          {
            label: "Total Interviews",
            value: String(data.total_interviews ?? 0),
            icon: MessagesSquare,
            change: `+${data.this_month ?? 0} this month`,
          },
          {
            label: "Average Score",
            value: String(data.average_score ?? 0),
            icon: Award,
            change: data.grade ?? "Grade A",
          },
          {
            label: "Current Streak",
            value: `${data.streak ?? 0}d`,
            icon: Flame,
            change: "Keep going!",
          },
          {
            label: "Improvement",
            value: `+${data.improvement ?? 0}%`,
            icon: TrendingUp,
            change: "vs last month",
          },
        ]);

        // Fetch chart data
        const chartRes = await API.get("/users/scores/");
        const chartList = Array.isArray(chartRes.data)
          ? chartRes.data
          : chartRes.data.results || [];
        setChartData(chartList);

        // Fetch recent sessions
        const sessionsRes = await API.get("/interviews/sessions/");
        const sessionsList = Array.isArray(sessionsRes.data)
          ? sessionsRes.data
          : sessionsRes.data.results || [];
        setRecent(sessionsList.slice(0, 4));

      } catch (err) {
        setError("Failed to load dashboard data");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  return (
    <AppShell>
      <div className="mx-auto max-w-6xl space-y-6 px-6 py-8 lg:px-10">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-extrabold md:text-4xl">Welcome back 👋</h1>
            <p className="mt-1 text-muted-foreground">Ready for another round?</p>
          </div>
          <Link to="/setup">
            <Button className="gradient-bg text-white border-0 glow-hover h-11">
              <Plus className="mr-2 h-4 w-4" /> Start New Interview
            </Button>
          </Link>
        </div>

        {error && (
          <div className="rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
            {error}
          </div>
        )}

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((s) => (
            <div key={s.label} className="glass-card glow-hover p-5">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">{s.label}</span>
                <span className="grid h-9 w-9 place-items-center rounded-lg gradient-bg">
                  <s.icon className="h-4 w-4 text-white" />
                </span>
              </div>
              <div className="mt-3 text-3xl font-extrabold">
                {loading ? "..." : s.value}
              </div>
              <div className="mt-1 text-xs text-muted-foreground">{s.change}</div>
            </div>
          ))}
        </div>

        <div className="glass-card p-6">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold">Performance</h2>
              <p className="text-xs text-muted-foreground">Last 7 days</p>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer>
              <LineChart data={chartData.length > 0 ? chartData : [
                { d: "Mon", score: 0 }, { d: "Tue", score: 0 },
                { d: "Wed", score: 0 }, { d: "Thu", score: 0 },
                { d: "Fri", score: 0 }, { d: "Sat", score: 0 },
                { d: "Sun", score: 0 },
              ]}>
                <defs>
                  <linearGradient id="lg" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="oklch(0.7 0.24 295)" />
                    <stop offset="100%" stopColor="oklch(0.7 0.22 240)" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="oklch(0.5 0.05 280 / 0.2)" />
                <XAxis dataKey="d" stroke="currentColor" className="text-muted-foreground text-xs" />
                <YAxis stroke="currentColor" className="text-muted-foreground text-xs" />
                <Tooltip contentStyle={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12 }} />
                <Line type="monotone" dataKey="score" stroke="url(#lg)" strokeWidth={3} dot={{ r: 5, fill: "oklch(0.7 0.24 295)" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-bold">Recent interviews</h2>
            <Link to="/results" className="text-sm text-primary inline-flex items-center gap-1 hover:underline">
              View all <ArrowUpRight className="h-3 w-3" />
            </Link>
          </div>
          <div className="overflow-x-auto">
            {loading ? (
              <p className="text-muted-foreground text-sm">Loading...</p>
            ) : recent.length === 0 ? (
              <p className="text-muted-foreground text-sm">
                No interviews yet. Start your first interview!
              </p>
            ) : (
              <table className="w-full text-sm">
                <thead className="text-left text-xs uppercase tracking-wider text-muted-foreground">
                  <tr>
                    <th className="py-3 font-medium">Role</th>
                    <th className="py-3 font-medium">Type</th>
                    <th className="py-3 font-medium">Score</th>
                    <th className="py-3 font-medium">Grade</th>
                    <th className="py-3 font-medium">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recent.map((r: any, i) => (
                    <tr key={i} className="border-t border-border/50 hover:bg-secondary/50 transition">
                      <td className="py-3 font-medium">{r.interview_type}</td>
                      <td className="py-3 text-muted-foreground">{r.difficulty}</td>
                      <td className="py-3 font-semibold">{r.overall_score ?? "-"}</td>
                      <td className="py-3">
                        <span className="rounded-md gradient-bg px-2 py-0.5 text-xs font-bold text-white">
                          {r.overall_score >= 80 ? "A" : r.overall_score >= 60 ? "B" : "C"}
                        </span>
                      </td>
                      <td className="py-3 text-muted-foreground">
                        {r.started_at ? new Date(r.started_at).toLocaleDateString() : "-"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}