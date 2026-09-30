from fastapi.testclient import TestClient

from lanedeck_backend.main import create_app


def test_cards_survive_new_app_same_database(tmp_path):
    db_url = f"sqlite:///{(tmp_path / 'persist.db').resolve().as_posix()}"

    app1 = create_app(db_url)
    with TestClient(app1) as client1:
        created = client1.post("/api/cards", json={"title": "Persists", "lane": "doing"}).json()
        assert created["title"] == "Persists"

    app2 = create_app(db_url)
    with TestClient(app2) as client2:
        cards = client2.get("/api/cards").json()
        assert len(cards) == 1
        assert cards[0]["id"] == created["id"]
        assert cards[0]["lane"] == "doing"
