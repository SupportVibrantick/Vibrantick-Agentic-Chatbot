import { motion, AnimatePresence } from "framer-motion";
import {
  Brain,
  Cpu,
  Database,
  FileSearch,
  Gauge,
  GitBranch,
  Plug,
  Zap,
} from "lucide-react";

export function RightPanel({ open }: { open: boolean }) {
  return (
    <AnimatePresence initial={false}>
      {open && (
        <motion.aside
          initial={{ x: 360, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: 360, opacity: 0 }}
          transition={{ type: "spring", stiffness: 260, damping: 30 }}
          className="glass-strong scrollbar-thin hidden lg:flex h-full w-80 shrink-0 flex-col gap-4 overflow-y-auto border-l border-border p-4"
        >
          <PanelHeader />

          <Card title="Agent Activity" icon={GitBranch}>
            <Timeline
              steps={[
                { label: "Planner", status: "done", detail: "Decomposed into 4 subtasks" },
                { label: "RAG Retrieval", status: "done", detail: "12 chunks · 0.42s" },
                { label: "Reasoning", status: "active", detail: "Analyzing Q3 report" },
                { label: "Synthesis", status: "pending", detail: "Waiting" },
              ]}
            />
          </Card>

          <div className="grid grid-cols-2 gap-3">
            <Stat icon={Zap} label="Latency" value="0.82s" tone="success" />
            <Stat icon={Gauge} label="Tokens" value="4,218" />
            <Stat icon={Cpu} label="Model" value="GPT-5.5" />
            <Stat icon={Database} label="Chunks" value="12" />
          </div>

          <Card title="Memory" icon={Brain}>
            <div className="space-y-2">
              <MemoryRow name="User preferences" size="24 KB" hot />
              <MemoryRow name="Nova Launch project" size="1.2 MB" hot />
              <MemoryRow name="Team style guide" size="86 KB" />
            </div>
          </Card>

          <Card title="Retrieved Sources" icon={FileSearch}>
            <div className="space-y-2">
              <SourceRow title="Q3-2025-Financials.pdf" page="p.14" score={0.94} />
              <SourceRow title="Board Memo — Nov" page="p.3" score={0.88} />
              <SourceRow title="Revenue-Segments.xlsx" page="Sheet 2" score={0.81} />
            </div>
          </Card>

          <Card title="Active Plugins" icon={Plug}>
            <div className="flex flex-wrap gap-1.5">
              {["Web Search", "Code Runner", "SQL", "Calendar", "Notion"].map((p) => (
                <span
                  key={p}
                  className="rounded-full border border-primary/30 bg-primary/10 px-2 py-0.5 text-[11px] font-medium text-foreground"
                >
                  {p}
                </span>
              ))}
            </div>
          </Card>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}

function PanelHeader() {
  return (
    <div>
      <div className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
        Assistant
      </div>
      <div className="mt-1 text-lg font-semibold">Live insights</div>
      <div className="text-xs text-muted-foreground">
        Real-time visibility into agents, memory, and tool calls.
      </div>
    </div>
  );
}

function Card({
  title,
  icon: Icon,
  children,
}: {
  title: string;
  icon: React.ComponentType<{ className?: string }>;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-border bg-card/50 p-3.5">
      <div className="mb-3 flex items-center gap-2 text-xs font-semibold text-foreground">
        <Icon className="h-3.5 w-3.5 text-primary" />
        {title}
      </div>
      {children}
    </div>
  );
}

function Stat({
  icon: Icon,
  label,
  value,
  tone,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: string;
  tone?: "success";
}) {
  return (
    <div className="rounded-xl border border-border bg-card/50 p-3">
      <div className="flex items-center gap-1.5 text-[10px] uppercase tracking-wider text-muted-foreground">
        <Icon className="h-3 w-3" />
        {label}
      </div>
      <div
        className={
          "mt-1 font-mono text-sm font-semibold " +
          (tone === "success" ? "text-success" : "text-foreground")
        }
      >
        {value}
      </div>
    </div>
  );
}

function Timeline({
  steps,
}: {
  steps: { label: string; status: "done" | "active" | "pending"; detail: string }[];
}) {
  return (
    <ol className="relative space-y-3 border-l border-border pl-4">
      {steps.map((s) => (
        <li key={s.label} className="relative">
          <span
            className={
              "absolute -left-[21px] top-1 h-2.5 w-2.5 rounded-full ring-4 ring-card " +
              (s.status === "done"
                ? "bg-success"
                : s.status === "active"
                  ? "bg-primary animate-pulse"
                  : "bg-muted-foreground/40")
            }
          />
          <div className="text-xs font-medium text-foreground">{s.label}</div>
          <div className="text-[11px] text-muted-foreground">{s.detail}</div>
        </li>
      ))}
    </ol>
  );
}

function MemoryRow({ name, size, hot }: { name: string; size: string; hot?: boolean }) {
  return (
    <div className="flex items-center gap-2 text-xs">
      <div
        className={
          "h-1.5 w-1.5 rounded-full " + (hot ? "bg-accent shadow-[0_0_6px_var(--accent)]" : "bg-muted-foreground/40")
        }
      />
      <span className="flex-1 truncate">{name}</span>
      <span className="font-mono text-muted-foreground">{size}</span>
    </div>
  );
}

function SourceRow({ title, page, score }: { title: string; page: string; score: number }) {
  return (
    <div className="flex items-center gap-2 rounded-lg border border-border bg-background/40 px-2 py-1.5 text-xs">
      <FileSearch className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
      <div className="min-w-0 flex-1">
        <div className="truncate font-medium">{title}</div>
        <div className="text-[10px] text-muted-foreground">{page}</div>
      </div>
      <span className="rounded-md bg-primary/15 px-1.5 py-0.5 font-mono text-[10px] text-primary">
        {score.toFixed(2)}
      </span>
    </div>
  );
}