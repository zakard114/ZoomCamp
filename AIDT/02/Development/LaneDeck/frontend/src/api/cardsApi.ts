import type { Card, CreateCardInput, Lane, UpdateCardInput } from "../types";

/** Base URL the frontend uses to talk to the backend (Homework Q6). */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Accept: "application/json",
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
      ...init?.headers,
    },
    ...init,
  });

  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`;
    try {
      const body = (await res.json()) as { detail?: unknown };
      if (typeof body.detail === "string") detail = body.detail;
      else if (body.detail !== undefined) detail = JSON.stringify(body.detail);
    } catch {
      // ignore non-JSON error bodies
    }
    throw new Error(detail);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return (await res.json()) as T;
}

/**
 * Central backend client for LaneDeck.
 * Talks to the FastAPI backend over HTTP.
 */
export const cardsApi = {
  async health(): Promise<{ status: string }> {
    return request<{ status: string }>("/health");
  },

  async listCards(lane?: Lane): Promise<Card[]> {
    const query = lane ? `?lane=${encodeURIComponent(lane)}` : "";
    return request<Card[]>(`/api/cards${query}`);
  },

  async createCard(input: CreateCardInput): Promise<Card> {
    return request<Card>("/api/cards", {
      method: "POST",
      body: JSON.stringify({
        title: input.title,
        ...(input.lane ? { lane: input.lane } : {}),
      }),
    });
  },

  async updateCard(id: string, input: UpdateCardInput): Promise<Card> {
    const body: UpdateCardInput = {};
    if (input.title !== undefined) body.title = input.title;
    if (input.lane !== undefined) body.lane = input.lane;
    if (input.position !== undefined) body.position = input.position;
    return request<Card>(`/api/cards/${encodeURIComponent(id)}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
  },

  async deleteCard(id: string): Promise<void> {
    await request<void>(`/api/cards/${encodeURIComponent(id)}`, {
      method: "DELETE",
    });
  },
};
