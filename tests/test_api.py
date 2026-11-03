from app import create_app

client = create_app().test_client()


def test_pages_render():
    for url in ["/", "/crop/wheat", "/weather", "/doctor"]:
        assert client.get(url).status_code == 200
    assert client.get("/crop/nope").status_code == 404


def test_crops_filter():
    data = client.get("/api/crops?season=Rabi").get_json()
    assert data and all(c["season"] == "Rabi" for c in data)


def test_diseases_and_advisory():
    assert client.get("/api/diseases?q=yellow stripes").get_json()[0]["crop_id"] == "wheat"
    r = client.get("/api/advisory?city=Delhi&crop=wheat").get_json()
    assert len(r["days"]) == 7 and r["advice"]
    assert client.get("/api/advisory?city=Mars").status_code == 400
