import type { ReactNode } from "react";
import { AppSidebar } from "./AppSidebar";
import { MeshBackground } from "./MeshBackground";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="relative flex min-h-screen">
      <MeshBackground />
      <AppSidebar />
      <main className="flex-1 animate-fade-in">{children}</main>
    </div>
  );
}