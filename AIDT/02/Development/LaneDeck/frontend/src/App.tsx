import { useCallback, useEffect, useMemo, useState } from "react";
import { cardsApi } from "./api/cardsApi";
import { Board } from "./components/Board";
import type { Card, Lane } from "./types";
import { LANES } from "./types";

export default function App() {
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const list = await cardsApi.listCards();
      setCards(list);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load board");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const byLane = useMemo(() => {
    const map: Record<Lane, Card[]> = { todo: [], doing: [], done: [] };
    for (const lane of LANES) {
      map[lane] = cards
        .filter((c) => c.lane === lane)
        .sort((a, b) => a.position - b.position);
    }
    return map;
  }, [cards]);

  async function handleCreate(lane: Lane, title: string) {
    setError(null);
    try {
      const card = await cardsApi.createCard({ title, lane });
      setCards((prev) => [...prev, card]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create card");
    }
  }

  async function handleRename(id: string, title: string) {
    setError(null);
    try {
      const card = await cardsApi.updateCard(id, { title });
      setCards((prev) => prev.map((c) => (c.id === id ? card : c)));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to rename card");
    }
  }

  async function handleMove(id: string, lane: Lane) {
    setError(null);
    try {
      const card = await cardsApi.updateCard(id, { lane });
      setCards((prev) => prev.map((c) => (c.id === id ? card : c)));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to move card");
    }
  }

  async function handleDelete(id: string) {
    setError(null);
    try {
      await cardsApi.deleteCard(id);
      setCards((prev) => prev.filter((c) => c.id !== id));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to delete card");
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand-block">
          <p className="brand">LaneDeck</p>
          <h1 className="tagline">Move work across lanes with clarity</h1>
        </div>
        <p className="subtitle">A lightweight Kanban for a handful of tasks</p>
      </header>

      {error ? (
        <div className="banner error" role="alert">
          {error}
          <button type="button" className="banner-dismiss" onClick={() => setError(null)}>
            Dismiss
          </button>
        </div>
      ) : null}

      {loading ? (
        <p className="loading">Loading board…</p>
      ) : (
        <Board
          byLane={byLane}
          onCreate={handleCreate}
          onRename={handleRename}
          onMove={handleMove}
          onDelete={handleDelete}
        />
      )}
    </div>
  );
}
