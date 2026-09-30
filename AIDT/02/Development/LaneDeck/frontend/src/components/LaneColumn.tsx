import { useState, type FormEvent } from "react";
import type { Card, Lane } from "../types";
import { LANE_LABELS } from "../types";
import { CardItem } from "./CardItem";

type Props = {
  lane: Lane;
  cards: Card[];
  onCreate: (lane: Lane, title: string) => Promise<void>;
  onRename: (id: string, title: string) => Promise<void>;
  onMove: (id: string, lane: Lane) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
};

export function LaneColumn({ lane, cards, onCreate, onRename, onMove, onDelete }: Props) {
  const [draft, setDraft] = useState("");
  const [adding, setAdding] = useState(false);
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!draft.trim() || busy) return;
    setBusy(true);
    try {
      await onCreate(lane, draft);
      setDraft("");
      setAdding(false);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className={`lane lane-${lane}`} aria-labelledby={`lane-${lane}`}>
      <div className="lane-head">
        <h2 id={`lane-${lane}`}>{LANE_LABELS[lane]}</h2>
        <span className="lane-count">{cards.length}</span>
      </div>

      <ul className="card-list">
        {cards.length === 0 ? (
          <li className="empty">No cards yet</li>
        ) : (
          cards.map((card) => (
            <CardItem
              key={card.id}
              card={card}
              onRename={onRename}
              onMove={onMove}
              onDelete={onDelete}
            />
          ))
        )}
      </ul>

      {adding ? (
        <form className="add-form" onSubmit={submit}>
          <input
            autoFocus
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="Card title"
            maxLength={200}
            aria-label={`New card in ${LANE_LABELS[lane]}`}
          />
          <div className="add-actions">
            <button type="submit" disabled={busy || !draft.trim()}>
              Add
            </button>
            <button
              type="button"
              className="ghost"
              onClick={() => {
                setAdding(false);
                setDraft("");
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <button type="button" className="add-trigger" onClick={() => setAdding(true)}>
          + Add card
        </button>
      )}
    </section>
  );
}
