export type Role = "user" | "assistant";

export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: string;
  liked?: boolean;
  disliked?: boolean;
}

export interface Conversation {
  id: string;
  title: string;
  updatedAt: string;
  pinned?: boolean;
  preview?: string;
}