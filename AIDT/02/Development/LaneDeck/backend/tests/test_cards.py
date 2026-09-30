def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_list_empty(client):
    res = client.get("/api/cards")
    assert res.status_code == 200
    assert res.json() == []


def test_create_card_defaults_to_todo(client):
    res = client.post("/api/cards", json={"title": "  Ship OpenAPI  "})
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Ship OpenAPI"
    assert body["lane"] == "todo"
    assert body["position"] == 0
    assert "id" in body
    assert "createdAt" in body
    assert "updatedAt" in body


def test_create_rejects_blank_title(client):
    res = client.post("/api/cards", json={"title": "   "})
    assert res.status_code == 422


def test_list_filter_by_lane(client):
    client.post("/api/cards", json={"title": "A", "lane": "todo"})
    client.post("/api/cards", json={"title": "B", "lane": "doing"})
    res = client.get("/api/cards", params={"lane": "doing"})
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["title"] == "B"


def test_update_rename_and_move(client):
    created = client.post("/api/cards", json={"title": "Draft"}).json()
    card_id = created["id"]

    renamed = client.patch(f"/api/cards/{card_id}", json={"title": "Ready"})
    assert renamed.status_code == 200
    assert renamed.json()["title"] == "Ready"

    moved = client.patch(f"/api/cards/{card_id}", json={"lane": "done"})
    assert moved.status_code == 200
    body = moved.json()
    assert body["lane"] == "done"
    assert body["position"] == 0


def test_delete_card(client):
    created = client.post("/api/cards", json={"title": "Temp"}).json()
    card_id = created["id"]

    deleted = client.delete(f"/api/cards/{card_id}")
    assert deleted.status_code == 204

    missing = client.get("/api/cards")
    assert missing.json() == []

    again = client.delete(f"/api/cards/{card_id}")
    assert again.status_code == 404


def test_update_missing_card(client):
    res = client.patch(
        "/api/cards/00000000-0000-0000-0000-000000000000",
        json={"title": "Nope"},
    )
    assert res.status_code == 404
