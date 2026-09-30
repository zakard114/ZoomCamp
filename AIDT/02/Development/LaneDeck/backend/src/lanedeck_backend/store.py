from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import get_session_factory
from .db_models import CardRow
from .models import Card, CreateCardRequest, Lane, UpdateCardRequest, utc_now


def _to_card(row: CardRow) -> Card:
    return Card(
        id=row.id,
        title=row.title,
        lane=Lane(row.lane),
        position=row.position,
        createdAt=row.created_at,
        updatedAt=row.updated_at,
    )


class CardStore:
    """SQLAlchemy-backed card store (SQLite by default)."""

    def _session(self) -> Session:
        return get_session_factory()()

    def clear(self) -> None:
        from sqlalchemy import delete

        with self._session() as session:
            session.execute(delete(CardRow))
            session.commit()

    def list_cards(self, lane: Optional[Lane] = None) -> list[Card]:
        with self._session() as session:
            stmt = select(CardRow)
            if lane is not None:
                stmt = stmt.where(CardRow.lane == lane.value)
            rows = session.scalars(stmt).all()
            lane_order = {Lane.todo.value: 0, Lane.doing.value: 1, Lane.done.value: 2}
            rows = sorted(
                rows,
                key=lambda r: (lane_order.get(r.lane, 99), r.position, r.created_at),
            )
            return [_to_card(r) for r in rows]

    def create(self, body: CreateCardRequest) -> Card:
        lane = body.lane or Lane.todo
        with self._session() as session:
            position = self._next_position(session, lane)
            stamp = utc_now()
            row = CardRow(
                id=str(uuid.uuid4()),
                title=body.title,
                lane=lane.value,
                position=position,
                created_at=stamp,
                updated_at=stamp,
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return _to_card(row)

    def update(self, card_id: str, body: UpdateCardRequest) -> Card:
        with self._session() as session:
            row = session.get(CardRow, card_id)
            if row is None:
                raise KeyError(card_id)

            if body.title is not None:
                row.title = body.title

            moving = body.lane is not None and body.lane.value != row.lane
            if body.lane is not None:
                row.lane = body.lane.value

            if body.position is not None:
                row.position = body.position
            elif moving and body.lane is not None:
                row.position = self._next_position(session, body.lane, exclude_id=card_id)

            row.updated_at = utc_now()
            session.commit()
            session.refresh(row)
            return _to_card(row)

    def delete(self, card_id: str) -> None:
        with self._session() as session:
            row = session.get(CardRow, card_id)
            if row is None:
                raise KeyError(card_id)
            session.delete(row)
            session.commit()

    def _next_position(
        self,
        session: Session,
        lane: Lane,
        exclude_id: Optional[str] = None,
    ) -> int:
        stmt = select(func.max(CardRow.position)).where(CardRow.lane == lane.value)
        if exclude_id is not None:
            stmt = stmt.where(CardRow.id != exclude_id)
        current = session.scalar(stmt)
        return 0 if current is None else int(current) + 1
