from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response

from .models import Card, CreateCardRequest, HealthResponse, Lane, UpdateCardRequest
from .store import CardStore

router = APIRouter()
store = CardStore()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/api/cards", response_model=list[Card])
def list_cards(lane: Optional[Lane] = Query(default=None)) -> list[Card]:
    return store.list_cards(lane)


@router.post("/api/cards", response_model=Card, status_code=201)
def create_card(body: CreateCardRequest) -> Card:
    return store.create(body)


@router.patch("/api/cards/{card_id}", response_model=Card)
def update_card(card_id: str, body: UpdateCardRequest) -> Card:
    try:
        return store.update(card_id, body)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Card not found") from exc


@router.delete("/api/cards/{card_id}", status_code=204)
def delete_card(card_id: str) -> Response:
    try:
        store.delete(card_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Card not found") from exc
    return Response(status_code=204)
