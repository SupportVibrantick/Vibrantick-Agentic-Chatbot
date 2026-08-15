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

function WorkspacePage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [rightOpen, setRightOpen] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [input, setInput] = useState("");

  const scrollRef = useRef<HTMLDivElement | null>(null);

  const abortController = useRef<AbortController | null>(
    null,
  );

  useEffect(() => {
    const el = scrollRef.current;

    if (el) {
      el.scrollTo({
        top: el.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  useEffect(() => {
    const mq = window.matchMedia(
      "(max-width: 1024px)",
    );

    const apply = () => {
      if (mq.matches) {
        setSidebarOpen(false);
        setRightOpen(false);
      }
    };

    apply();

    mq.addEventListener(
      "change",
      apply,
    );

    return () =>
      mq.removeEventListener(
        "change",
        apply,
      );
  }, []);

  const send = async (
    text: string,
  ) => {
    if (!text.trim()) return;

    const now =
      new Date().toLocaleTimeString(
        [],
        {
          hour: "2-digit",
          minute: "2-digit",
        },
      );

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      timestamp: now,
    };

    const assistantId =
      crypto.randomUUID();

    setMessages((previous) => [
      ...previous,
      userMessage,
      {
        id: assistantId,
        role: "assistant",
        content: "",
        timestamp: now,
      },
    ]);

    setStreaming(true);

    abortController.current =
      new AbortController();

    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
      const token = localStorage.getItem("access_token") || "";
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(`${baseUrl}/api/chat/stream`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          chatbot_id: 1,
          message: text,
        }),
        signal: abortController.current.signal,
      });

      if (!response.ok) {
        throw new Error(
          "Backend returned an error.",
        );
      }

      if (!response.body) {
        throw new Error(
          "Streaming not supported.",
        );
      }

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let answer = "";

      while (true) {
        const {
          done,
          value,
        } = await reader.read();

        if (done) {
          break;
        }

        answer += decoder.decode(
          value,
          {
            stream: true,
          },
        );

        setMessages(
          (previous) =>
            previous.map(
              (message) =>
                message.id ===
                assistantId
                  ? {
                      ...message,
                      content: answer,
                    }
                  : message,
            ),
        );
      }
    } catch (error) {
      console.error(error);

      setMessages(
        (previous) =>
          previous.map(
            (message) =>
              message.id ===
              assistantId
                ? {
                    ...message,
                    content:
                      "Unable to contact the AI server.",
                  }
                : message,
          ),
      );
    } finally {
      setStreaming(false);
      abortController.current =
        null;
    }
  };

  const stop = () => {
    abortController.current?.abort();
    setStreaming(false);
  };

  const isEmpty =
    messages.length === 0;

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar
        open={sidebarOpen}
      />

      <div className="relative flex min-w-0 flex-1 flex-col">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 opacity-60"
          style={{
            background:
              "var(--gradient-glow)",
          }}
        />

        <div className="relative z-10 flex h-full min-w-0 flex-col">
          <TopNav
            onToggleSidebar={() =>
              setSidebarOpen(
                (value) => !value,
              )
            }
            onToggleRight={() =>
              setRightOpen(
                (value) => !value,
              )
            }
          />

          <div
            ref={scrollRef}
            className="scrollbar-thin flex-1 overflow-y-auto"
          >
            {isEmpty ? (
              <WelcomeScreen
                onPick={(prompt) =>
                  setInput(prompt)
                }
              />
            ) : (
              <MessageList
                messages={messages}
                streaming={streaming}
              />
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

      <RightPanel
        open={rightOpen}
      />
    </div>
  );
}