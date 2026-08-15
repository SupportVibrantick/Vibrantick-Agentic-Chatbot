import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Bot, Sliders, Sparkles } from "lucide-react";

interface ChatbotConfigModalProps {
  open: boolean;
  onClose: () => void;
}

export function ChatbotConfigModal({ open, onClose }: ChatbotConfigModalProps) {
  const [model, setModel] = useState("deepseek-chat");
  const [temperature, setTemperature] = useState(0.7);
  const [systemPrompt, setSystemPrompt] = useState(
    "You are an AI assistant that answers questions accurately using the provided knowledge base context."
  );
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => {
      setSaved(false);
      onClose();
    }, 800);
  };

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="w-full max-w-lg rounded-2xl border border-border bg-background/95 p-6 shadow-2xl backdrop-blur-xl"
          >
            <div className="flex items-center justify-between pb-4 border-b border-border">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Bot className="h-5 w-5 text-primary" />
                Chatbot & AI Configuration
              </h2>
              <button onClick={onClose} className="rounded-lg p-1 text-muted-foreground hover:bg-muted">
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={handleSave} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">LLM Model</label>
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full rounded-xl border border-border bg-muted/40 px-3 py-2 text-sm focus:border-primary focus:outline-none"
                >
                  <option value="deepseek-chat">DeepSeek Chat (deepseek-chat)</option>
                  <option value="gpt-4o-mini">OpenAI GPT-4o Mini</option>
                  <option value="gpt-4o">OpenAI GPT-4o</option>
                </select>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-muted-foreground flex items-center gap-1">
                    <Sliders className="h-3.5 w-3.5" /> Temperature
                  </label>
                  <span className="text-xs font-mono text-primary font-semibold">{temperature}</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={temperature}
                  onChange={(e) => setTemperature(parseFloat(e.target.value))}
                  className="w-full accent-primary"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">System Instructions</label>
                <textarea
                  rows={4}
                  value={systemPrompt}
                  onChange={(e) => setSystemPrompt(e.target.value)}
                  className="w-full rounded-xl border border-border bg-muted/40 p-3 text-sm focus:border-primary focus:outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full rounded-xl bg-gradient-primary py-2.5 text-sm font-semibold text-primary-foreground shadow-glow hover:opacity-90 transition"
              >
                {saved ? "Saved Configuration!" : "Save Settings"}
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
