import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import {
  Copy,
  Pencil,
  RefreshCw,
  ThumbsUp,
  ThumbsDown,
  Share2,
  Trash2,
  Sparkles,
} from "lucide-react";
import type { Message } from "./types";
import { cn } from "@/lib/utils";

export function MessageList({
  messages,
  streaming,
}: {
  messages: Message[];
  streaming: boolean;
}) {
  return (
    <div className="scrollbar-thin mx-auto flex w-full max-w-3xl flex-col gap-8 px-4 py-8">
      {messages.map((m) => (
        <MessageBubble key={m.id} message={m} />
      ))}
      {streaming && <TypingIndicator />}
    </div>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className={cn("group flex gap-3", isUser && "flex-row-reverse")}
    >
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-semibold",
          isUser
            ? "bg-muted text-foreground"
            : "bg-gradient-primary text-primary-foreground shadow-glow",
        )}
      >
        {isUser ? "AR" : <Sparkles className="h-4 w-4" />}
      </div>

      <div className={cn("flex min-w-0 max-w-[85%] flex-col", isUser && "items-end")}>
        <div
          className={cn(
            "prose prose-sm prose-invert max-w-none rounded-2xl px-4 py-3 text-[15px] leading-relaxed",
            isUser
              ? "bg-primary text-primary-foreground rounded-tr-md"
              : "glass rounded-tl-md text-foreground",
          )}
        >
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        <div className="mt-1.5 flex items-center gap-1 text-[11px] text-muted-foreground opacity-0 group-hover:opacity-100 transition">
          <span className="mr-2 font-mono">{message.timestamp}</span>
          <ActionBtn icon={Copy} label="Copy" />
          {isUser ? (
            <>
              <ActionBtn icon={Pencil} label="Edit" />
              <ActionBtn icon={Trash2} label="Delete" />
            </>
          ) : (
            <>
              <ActionBtn icon={RefreshCw} label="Regenerate" />
              <ActionBtn icon={ThumbsUp} label="Like" />
              <ActionBtn icon={ThumbsDown} label="Dislike" />
              <ActionBtn icon={Share2} label="Share" />
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
}

function ActionBtn({
  icon: Icon,
  label,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
}) {
  return (
    <button
      aria-label={label}
      title={label}
      className="rounded-md p-1 hover:bg-muted hover:text-foreground transition"
    >
      <Icon className="h-3.5 w-3.5" />
    </button>
  );
}

function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex items-center gap-3"
    >
      <div className="bg-gradient-primary shadow-glow flex h-8 w-8 items-center justify-center rounded-full text-primary-foreground">
        <Sparkles className="h-4 w-4" />
      </div>
      <div className="glass flex items-center gap-1.5 rounded-2xl rounded-tl-md px-4 py-3">
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            className="h-1.5 w-1.5 rounded-full bg-muted-foreground"
            animate={{ opacity: [0.3, 1, 0.3], y: [0, -2, 0] }}
            transition={{ duration: 1, repeat: Infinity, delay: i * 0.15 }}
          />
        ))}
        <span className="ml-2 text-xs text-muted-foreground">Thinking…</span>
      </div>
    </motion.div>
  );
}