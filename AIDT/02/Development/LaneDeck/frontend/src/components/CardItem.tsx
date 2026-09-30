import { useState, type FormEvent } from "react";
import type { Card, Lane } from "../types";
import { LANE_LABELS, LANES } from "../types";

type Props = {
  card: Card;
  onRename: (id: string, title: string) => Promise<void>;
  onMove: (id: string, lane: Lane) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
};

export function CardItem({ card, onRename, onMove, onDelete }: Props) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(card.title);
  const [busy, setBusy] = useState(false);

  async function saveTitle(e: FormEvent) {
    e.preventDefault();
    if (!title.trim() || busy) return;
    setBusy(true);
    try {
      await onRename(card.id, title);
      setEditing(false);
    } finally {
      setBusy(false);
    }
  }

  async function moveTo(lane: Lane) {
    if (lane === card.lane || busy) return;
    setBusy(true);
    try {
      await onMove(card.id, lane);
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (busy) return;
    if (!window.confirm(`Delete “${card.title}”?`)) return;
    setBusy(true);
    try {
      await onDelete(card.id);
    } finally {
      setBusy(false);
    }
  }

  return (
    <li className="card">
      {editing ? (
        <form onSubmit={saveTitle} className="edit-form">
          <input
            autoFocus
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength={200}
            aria-label="Edit card title"
          />
          <div className="card-actions">
            <button type="submit" disabled={busy || !title.trim()}>
              Save
            </button>
            <button
              type="button"
              className="ghost"
              onClick={() => {
                setTitle(card.title);
                setEditing(false);
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <>
          <p className="card-title">{card.title}</p>
          <div className="card-actions">
            <button type="button" className="ghost" onClick={() => setEditing(true)}>
              Edit
            </button>
            <label className="move-label">
              <span className="sr-only">Move to</span>
              <select
                value={card.lane}
                disabled={busy}
                onChange={(e) => void moveTo(e.target.value as Lane)}
                aria-label={`Move ${card.title}`}
              >
                {LANES.map((lane) => (
                  <option key={lane} value={lane}>
                    {LANE_LABELS[lane]}
                  </option>
                ))}
              </select>
            </label>
            <button type="button" className="danger ghost" onClick={() => void remove()}>
              Delete
            </button>
          </div>
        </>
      )}
    </li>
  );
}
