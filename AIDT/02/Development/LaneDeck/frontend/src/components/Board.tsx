import type { Card, Lane } from "../types";
import { LANES } from "../types";
import { LaneColumn } from "./LaneColumn";

type Props = {
  byLane: Record<Lane, Card[]>;
  onCreate: (lane: Lane, title: string) => Promise<void>;
  onRename: (id: string, title: string) => Promise<void>;
  onMove: (id: string, lane: Lane) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
};

export function Board({ byLane, onCreate, onRename, onMove, onDelete }: Props) {
  return (
    <main className="board">
      {LANES.map((lane) => (
        <LaneColumn
          key={lane}
          lane={lane}
          cards={byLane[lane]}
          onCreate={onCreate}
          onRename={onRename}
          onMove={onMove}
          onDelete={onDelete}
        />
      ))}
    </main>
  );
}
