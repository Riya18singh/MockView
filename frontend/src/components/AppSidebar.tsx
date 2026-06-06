import { Link, useRouterState } from "@tanstack/react-router";
import { LayoutDashboard, PlayCircle, BarChart3, Settings, Sparkles, LogOut, Moon, Sun } from "lucide-react";
import { useTheme } from "@/lib/theme";
import { cn } from "@/lib/utils";

const items = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/setup", label: "New Interview", icon: PlayCircle },
  { to: "/results", label: "Results", icon: BarChart3 },
];

export function AppSidebar() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const { theme, toggle } = useTheme();
  return (
    <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-border/60 bg-card/40 backdrop-blur-xl lg:flex">
      <Link to="/" className="flex items-center gap-2 px-6 py-5">
        <span className="grid h-9 w-9 place-items-center rounded-xl gradient-bg glow">
          <Sparkles className="h-5 w-5 text-white" />
        </span>
        <span className="text-lg font-extrabold">MockView</span>
      </Link>
      <nav className="flex-1 space-y-1 px-3">
        {items.map((it) => {
          const active = pathname === it.to || (it.to !== "/dashboard" && pathname.startsWith(it.to));
          return (
            <Link
              key={it.to}
              to={it.to}
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition",
                active
                  ? "gradient-bg text-white glow"
                  : "text-muted-foreground hover:bg-secondary hover:text-foreground"
              )}
            >
              <it.icon className="h-4 w-4" />
              {it.label}
            </Link>
          );
        })}
      </nav>
      <div className="space-y-1 border-t border-border/60 p-3">
        <button
          onClick={toggle}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-muted-foreground hover:bg-secondary hover:text-foreground transition"
        >
          {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          {theme === "dark" ? "Light mode" : "Dark mode"}
        </button>
        <button className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-muted-foreground hover:bg-secondary hover:text-foreground transition">
          <Settings className="h-4 w-4" /> Settings
        </button>
        <button className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-muted-foreground hover:bg-secondary hover:text-foreground transition">
          <LogOut className="h-4 w-4" /> Logout
        </button>
      </div>
    </aside>
  );
}