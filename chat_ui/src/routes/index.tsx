import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopNav } from "@/components/layout/TopNav";
import { RightPanel } from "@/components/layout/RightPanel";
import { WelcomeScreen } from "@/features/chat/WelcomeScreen";
import { MessageList } from "@/features/chat/MessageList";
import { ChatInput } from "@/features/chat/ChatInput";
import type { Message } from "@/features/chat/types";

export const Route = createFileRoute("/")({
  component: WorkspacePage,
});

const DEMO_REPLY = `Here's a **quick breakdown** of Q4 revenue vs Q3:

| Segment    | Q3     | Q4     | Δ    |
| ---------- | ------ | ------ | ---- |
| Enterprise | $4.2M  | $5.1M  | +21% |
| Mid-market | $2.1M  | $2.4M  | +14% |
| Self-serve | $0.9M  | $1.1M  | +22% |

**Key drivers**

1. Nova launch accelerated enterprise pipeline
2. Self-serve activation up after onboarding revamp
3. Churn dropped to 1.4% (from 2.1%)

\`\`\`sql
select segment, sum(mrr) as revenue
from subscriptions
where quarter = 'Q4-2025'
group by 1 order by 2 desc;
\`\`\`

Want me to draft the board update from this?`;

function WorkspacePage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [rightOpen, setRightOpen] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [messages, streaming]);

  // Responsive defaults
  useEffect(() => {
    const mq = window.matchMedia("(max-width: 1024px)");
    const apply = () => {
      if (mq.matches) {
        setSidebarOpen(false);
        setRightOpen(false);
      }
    };
    apply();
    mq.addEventListener("change", apply);
    return () => mq.removeEventListener("change", apply);
  }, []);

  const send = (text: string) => {
    const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      timestamp: now,
    };
    const aiId = crypto.randomUUID();
    setMessages((m) => [
      ...m,
      userMsg,
      { id: aiId, role: "assistant", content: "", timestamp: now },
    ]);
    setStreaming(true);

    // Simulate token streaming
    let i = 0;
    const stream = () => {
      i += Math.max(2, Math.floor(Math.random() * 6));
      const partial = DEMO_REPLY.slice(0, i);
      setMessages((m) =>
        m.map((msg) => (msg.id === aiId ? { ...msg, content: partial } : msg)),
      );
      if (i < DEMO_REPLY.length) {
        timerRef.current = setTimeout(stream, 18);
      } else {
        setStreaming(false);
      }
    };
    timerRef.current = setTimeout(stream, 400);
  };

  const stop = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
    setStreaming(false);
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background text-foreground">
      <Sidebar open={sidebarOpen} />

      <div className="relative flex min-w-0 flex-1 flex-col">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 opacity-60"
          style={{ background: "var(--gradient-glow)" }}
        />
        <div className="relative z-10 flex h-full min-w-0 flex-col">
          <TopNav
            onToggleSidebar={() => setSidebarOpen((v) => !v)}
            onToggleRight={() => setRightOpen((v) => !v)}
          />

          <div
            ref={scrollRef}
            className="scrollbar-thin flex-1 overflow-y-auto"
          >
            {isEmpty ? (
              <WelcomeScreen onPick={(p) => setInput(p)} />
            ) : (
              <MessageList messages={messages} streaming={streaming} />
            )}
          </div>

          <ChatInput
            onSend={send}
            onStop={stop}
            streaming={streaming}
            value={input}
            setValue={setInput}
          />
        </div>
      </div>

      <RightPanel open={rightOpen} />
    </div>
  );
}
