import { Bell, Search, PanelLeft, PanelRight, ChevronDown, Command } from "lucide-react";

export function TopNav({
  onToggleSidebar,
  onToggleRight,
}: {
  onToggleSidebar: () => void;
  onToggleRight: () => void;
}) {
  return (
    <header className="glass sticky top-0 z-20 flex h-14 items-center gap-3 border-b border-border px-3 sm:px-5">
      <button
        onClick={onToggleSidebar}
        className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground transition"
        aria-label="Toggle sidebar"
      >
        <PanelLeft className="h-4 w-4" />
      </button>

      <div className="hidden sm:flex items-center gap-2 text-sm">
        <span className="text-muted-foreground">Nova Launch</span>
        <span className="text-muted-foreground/50">/</span>
        <span className="font-medium">Q4 revenue forecast breakdown</span>
      </div>

      <div className="ml-auto flex items-center gap-2">
        <button className="hidden md:flex items-center gap-2 rounded-lg border border-border bg-muted/40 px-2.5 py-1.5 text-xs font-medium hover:bg-muted transition">
          <div className="h-2 w-2 rounded-full bg-success shadow-[0_0_8px_var(--success)]" />
          <span>GPT-5.5 Turbo</span>
          <ChevronDown className="h-3 w-3 text-muted-foreground" />
        </button>

        <button className="hidden lg:flex items-center gap-2 rounded-lg border border-border bg-muted/40 px-2.5 py-1.5 text-xs text-muted-foreground hover:bg-muted transition">
          <Search className="h-3.5 w-3.5" />
          <span>Search</span>
          <span className="flex items-center gap-0.5 rounded bg-background px-1 font-mono text-[10px]">
            <Command className="h-2.5 w-2.5" />K
          </span>
        </button>

        <button
          className="relative rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground transition"
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4" />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-accent" />
        </button>

        <button
          onClick={onToggleRight}
          className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground transition"
          aria-label="Toggle right panel"
        >
          <PanelRight className="h-4 w-4" />
        </button>

        <div className="bg-gradient-primary ml-1 flex h-8 w-8 items-center justify-center rounded-full text-xs font-semibold text-primary-foreground">
          AR
        </div>
      </div>
    </header>
  );
}