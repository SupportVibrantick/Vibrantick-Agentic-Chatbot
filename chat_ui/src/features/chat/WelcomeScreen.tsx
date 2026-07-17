import { motion } from "framer-motion";
import { Bot, Code2, FileText, Database, Sparkles, Search } from "lucide-react";

const suggestions = [
  { icon: Bot, title: "Create a chatbot", desc: "Multi-agent flow with tools & memory" },
  { icon: Code2, title: "Explain code", desc: "Walk through a React component" },
  { icon: FileText, title: "Analyze document", desc: "Summarize a 40-page PDF" },
  { icon: Database, title: "SQL query", desc: "Cohort retention over 12 weeks" },
  { icon: Sparkles, title: "Generate UI", desc: "A pricing section with 3 tiers" },
  { icon: Search, title: "Research topic", desc: "Latest on RAG evaluation" },
];

export function WelcomeScreen({ onPick }: { onPick: (prompt: string) => void }) {
  return (
    <div className="relative mx-auto flex w-full max-w-3xl flex-1 flex-col items-center justify-center px-4 py-10">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-x-0 top-0 h-72"
        style={{ background: "var(--gradient-glow)" }}
      />

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative text-center"
      >
        <div className="bg-gradient-primary shadow-glow mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-2xl">
          <Sparkles className="h-7 w-7 text-primary-foreground" />
        </div>
        <h1 className="text-balance text-4xl font-bold tracking-tight sm:text-5xl">
          What can I help you <span className="text-gradient">build</span> today?
        </h1>
        <p className="mx-auto mt-3 max-w-lg text-sm text-muted-foreground sm:text-base">
          Ask anything, drop a file, or pick a starting point. Nexus routes across
          multiple agents and your knowledge base.
        </p>
      </motion.div>

      <motion.div
        initial="hidden"
        animate="show"
        variants={{
          hidden: {},
          show: { transition: { staggerChildren: 0.05, delayChildren: 0.2 } },
        }}
        className="relative mt-10 grid w-full grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3"
      >
        {suggestions.map(({ icon: Icon, title, desc }) => (
          <motion.button
            key={title}
            onClick={() => onPick(title + ": " + desc)}
            variants={{ hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0 } }}
            whileHover={{ y: -2 }}
            className="glass group rounded-2xl p-4 text-left transition hover:border-primary/40 hover:shadow-glow"
          >
            <div className="flex items-center gap-2">
              <div className="rounded-lg bg-primary/15 p-1.5 text-primary group-hover:bg-primary/25 transition">
                <Icon className="h-4 w-4" />
              </div>
              <div className="text-sm font-semibold">{title}</div>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">{desc}</p>
          </motion.button>
        ))}
      </motion.div>
    </div>
  );
}