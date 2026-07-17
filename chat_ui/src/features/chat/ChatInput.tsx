import { useRef, useEffect, useState } from "react";
import { Paperclip, Mic, Send, Smile, Square, Sparkles } from "lucide-react";

export function ChatInput({
  onSend,
  streaming,
  onStop,
  value,
  setValue,
}: {
  onSend: (text: string) => void;
  streaming: boolean;
  onStop: () => void;
  value: string;
  setValue: (v: string) => void;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  const [focused, setFocused] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 220) + "px";
  }, [value]);

  useEffect(() => {
    ref.current?.focus();
  }, []);

  const submit = () => {
    const t = value.trim();
    if (!t || streaming) return;
    onSend(t);
    setValue("");
  };

  return (
    <div className="mx-auto w-full max-w-3xl px-4 pb-6">
      <div
        className={
          "glass-strong relative rounded-3xl border transition " +
          (focused ? "border-primary/50 shadow-glow" : "border-border")
        }
      >
        <textarea
          ref={ref}
          rows={1}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              submit();
            }
          }}
          placeholder="Ask anything..."
          className="scrollbar-thin block w-full resize-none bg-transparent px-5 pt-4 pb-2 text-[15px] leading-6 placeholder:text-muted-foreground focus:outline-none"
        />
        <div className="flex items-center gap-1 px-2.5 pb-2.5">
          <IconBtn icon={Paperclip} label="Attach" />
          <IconBtn icon={Mic} label="Voice" />
          <IconBtn icon={Smile} label="Emoji" />
          <button className="ml-1 hidden sm:flex items-center gap-1 rounded-full border border-border px-2 py-1 text-[11px] font-medium text-muted-foreground hover:bg-muted transition">
            <Sparkles className="h-3 w-3 text-primary" /> Auto
          </button>

          <div className="ml-auto flex items-center gap-2">
            <span className="hidden sm:block text-[11px] text-muted-foreground">
              <kbd className="rounded bg-muted px-1 font-mono">⇧</kbd> +{" "}
              <kbd className="rounded bg-muted px-1 font-mono">Enter</kbd> for newline
            </span>
            {streaming ? (
              <button
                onClick={onStop}
                className="flex h-9 w-9 items-center justify-center rounded-full border border-border bg-muted hover:bg-destructive/20 hover:text-destructive transition"
                aria-label="Stop generation"
              >
                <Square className="h-3.5 w-3.5" />
              </button>
            ) : (
              <button
                onClick={submit}
                disabled={!value.trim()}
                className="bg-gradient-primary shadow-glow flex h-9 w-9 items-center justify-center rounded-full text-primary-foreground transition disabled:opacity-40 disabled:shadow-none"
                aria-label="Send"
              >
                <Send className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      </div>
      <p className="mt-2 text-center text-[11px] text-muted-foreground">
        Nexus can make mistakes. Verify important information.
      </p>
    </div>
  );
}

function IconBtn({
  icon: Icon,
  label,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
}) {
  return (
    <button
      aria-label={label}
      className="flex h-8 w-8 items-center justify-center rounded-full text-muted-foreground hover:bg-muted hover:text-foreground transition"
    >
      <Icon className="h-4 w-4" />
    </button>
  );
}