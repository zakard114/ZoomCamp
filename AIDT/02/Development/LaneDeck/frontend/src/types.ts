export type Lane = "todo" | "doing" | "done";

export const LANES: readonly Lane[] = ["todo", "doing", "done"] as const;

export const LANE_LABELS: Record<Lane, string> = {
  todo: "Todo",
  doing: "Doing",
  done: "Done",
};

export type Card = {
  id: string;
  title: string;
  lane: Lane;
  position: number;
  createdAt: string;
  updatedAt: string;
};

export type CreateCardInput = {
  title: string;
  lane?: Lane;
};

export type UpdateCardInput = {
  title?: string;
  lane?: Lane;
  position?: number;
};
