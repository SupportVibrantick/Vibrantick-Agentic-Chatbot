import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Plus,
  Search,
  Pin,
  MessageSquare,
  BookOpen,
  FileText,
  Bot,
  Store,
  BarChart3,
  Settings,
  Sparkles,
  ChevronDown,
  HardDrive,
  Moon,
  Sun,
  LogIn,
} from "lucide-react";
import { pinnedConversations, recentConversations } from "@/features/chat/data";
import { cn } from "@/lib/utils";
import { AuthModal } from "../auth/AuthModal";
import { KnowledgeBaseModal } from "../knowledge/KnowledgeBaseModal";
import { ChatbotConfigModal } from "../chatbot/ChatbotConfigModal";

export function Sidebar({ open }: { open: boolean }) {
  const [dark, setDark] = useState(true);
  const [query, setQuery] = useState("");
  const [authOpen, setAuthOpen] = useState(false);
  const [kbOpen, setKbOpen] = useState(false);
  const [configOpen, setConfigOpen] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);

  const handleNavClick = (label: string) => {
    if (label === "Knowledge Base" || label === "Documents") {
      setKbOpen(true);
    } else if (label === "Agents" || label === "Settings") {
      setConfigOpen(true);
    }
  };

  const navItems = [
    { icon: BookOpen, label: "Knowledge Base", badge: "Live" },
    { icon: FileText, label: "Documents" },
    { icon: Bot, label: "Agents", badge: "DeepSeek" },
    { icon: Store, label: "Marketplace" },
    { icon: BarChart3, label: "Analytics" },
    { icon: Settings, label: "Settings" },
  ];

  return (
    <>
      <AnimatePresence initial={false}>
        {open && (
          <motion.aside
            initial={{ x: -320, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -320, opacity: 0 }}
            transition={{ type: "spring", stiffness: 260, damping: 30 }}
            className="glass-strong scrollbar-thin relative z-30 flex h-full w-72 shrink-0 flex-col border-r border-border overflow-y-auto"
          >
            {/* Logo + Workspace */}
            <div className="flex items-center gap-3 px-4 pt-5 pb-3">
              <div className="bg-gradient-primary shadow-glow flex h-9 w-9 items-center justify-center rounded-xl">
                <Sparkles className="h-5 w-5 text-primary-foreground" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="truncate text-sm font-semibold">Nexus AI</div>
                <div className="text-xs text-muted-foreground truncate">Vibrantic Workspace</div>
              </div>
              <button className="rounded-md p-1 text-muted-foreground hover:bg-muted hover:text-foreground transition">
                <ChevronDown className="h-4 w-4" />
              </button>
            </div>

            <div className="px-3">
              <button className="bg-gradient-primary hover:opacity-95 group flex w-full items-center gap-2 rounded-xl px-3 py-2.5 text-sm font-medium text-primary-foreground shadow-glow transition">
                <Plus className="h-4 w-4" />
                New Chat
                <span className="ml-auto rounded-md bg-black/20 px-1.5 py-0.5 text-[10px] font-mono">
                  ⌘K
                </span>
              </button>
            </div>

            <div className="px-3 pt-3">
              <div className="relative">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search conversations"
                  className="w-full rounded-lg border border-border bg-muted/40 pl-9 pr-3 py-2 text-sm placeholder:text-muted-foreground focus:border-primary/50 focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
            </div>

            {/* Pinned */}
            <SidebarSection title="Pinned" icon={Pin}>
              {pinnedConversations.map((c) => (
                <ConversationRow key={c.id} title={c.title} updated={c.updatedAt} active={c.id === "c1"} />
              ))}
            </SidebarSection>

            {/* Recent */}
            <SidebarSection title="Recent" icon={MessageSquare}>
              {recentConversations.map((c) => (
                <ConversationRow key={c.id} title={c.title} updated={c.updatedAt} />
              ))}
            </SidebarSection>

            {/* Nav */}
            <div className="mt-2 border-t border-border/60 pt-3 px-2 space-y-0.5">
              {navItems.map(({ icon: Icon, label, badge }) => (
                <button
                  key={label}
                  onClick={() => handleNavClick(label)}
                  className={cn(
                    "group flex w-full items-center gap-3 rounded-lg px-2.5 py-2 text-sm text-muted-foreground hover:bg-muted/60 hover:text-foreground transition"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="flex-1 text-left">{label}</span>
                  {badge && (
                    <span className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground">
                      {badge}
                    </span>
                  )}
                </button>
              ))}
            </div>

            {/* Storage */}
            <div className="mx-3 mt-4 rounded-xl border border-border bg-muted/30 p-3">
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <HardDrive className="h-3.5 w-3.5" />
                <span>Storage</span>
                <span className="ml-auto font-mono text-foreground">6.4 / 20 GB</span>
              </div>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-background">
                <div className="bg-gradient-primary h-full" style={{ width: "32%" }} />
              </div>
            </div>

            {/* Profile / Auth */}
            <div className="mt-auto p-3">
              <div className="flex items-center gap-3 rounded-xl border border-border bg-muted/30 p-2 pr-3">
                <div className="bg-gradient-primary flex h-8 w-8 items-center justify-center rounded-full text-xs font-semibold text-primary-foreground">
                  {userEmail ? userEmail.slice(0, 2).toUpperCase() : "AI"}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="truncate text-sm font-medium">{userEmail || "Guest User"}</div>
                  <button
                    onClick={() => setAuthOpen(true)}
                    className="text-xs text-primary hover:underline flex items-center gap-1"
                  >
                    <LogIn className="h-3 w-3" /> {userEmail ? "Account" : "Sign In / Register"}
                  </button>
                </div>
                <button
                  onClick={() => setDark((d) => !d)}
                  className="rounded-md p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground transition"
                  aria-label="Toggle theme"
                >
                  {dark ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} onSuccess={(_, email) => setUserEmail(email)} />
      <KnowledgeBaseModal open={kbOpen} onClose={() => setKbOpen(false)} />
      <ChatbotConfigModal open={configOpen} onClose={() => setConfigOpen(false)} />
    </>
  );
}

function SidebarSection({
  title,
  icon: Icon,
  children,
}: {
  title: string;
  icon: React.ComponentType<{ className?: string }>;
  children: React.ReactNode;
}) {
  return (
    <div className="px-2 pt-4">
      <div className="flex items-center gap-2 px-2 pb-1.5 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
        <Icon className="h-3 w-3" />
        {title}
      </div>
      <div className="space-y-0.5">{children}</div>
    </div>
  );
}

function ConversationRow({
  title,
  updated,
  active,
}: {
  title: string;
  updated: string;
  active?: boolean;
}) {
  return (
    <button
      className={cn(
        "group flex w-full items-center gap-2 rounded-lg px-2.5 py-2 text-left text-sm transition",
        active
          ? "bg-primary/15 text-foreground ring-1 ring-primary/30"
          : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
      )}
    >
      <span className="truncate flex-1">{title}</span>
      <span className="text-[10px] font-mono text-muted-foreground shrink-0">{updated}</span>
    </button>
  );
}