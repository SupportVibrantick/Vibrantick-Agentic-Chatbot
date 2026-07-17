import type { Conversation, Message } from "./types";

export const pinnedConversations: Conversation[] = [
  {
    id: "c1",
    title: "Q4 revenue forecast breakdown",
    updatedAt: "2h",
    pinned: true,
    preview: "Compare 2024 vs 2025 by segment",
  },
  {
    id: "c2",
    title: "React Server Components deep dive",
    updatedAt: "5h",
    pinned: true,
    preview: "Explain hydration boundaries",
  },
];

export const recentConversations: Conversation[] = [
  { id: "c3", title: "Onboarding email sequence", updatedAt: "Yesterday" },
  { id: "c4", title: "Postgres index tuning", updatedAt: "Yesterday" },
  { id: "c5", title: "Product launch brief — Nova", updatedAt: "2d" },
  { id: "c6", title: "Meeting notes → action items", updatedAt: "3d" },
  { id: "c7", title: "Competitor pricing research", updatedAt: "5d" },
  { id: "c8", title: "Terraform module refactor", updatedAt: "1w" },
  { id: "c9", title: "Brand voice guidelines v2", updatedAt: "1w" },
  { id: "c10", title: "SQL: cohort retention query", updatedAt: "2w" },
];

export const seedMessages: Message[] = [];