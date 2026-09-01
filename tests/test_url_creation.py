def test_url_creation(client):
  response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com",
      "expires_at": None
    }
  )


  assert response.status_code == 201

  data = response.json()

  assert data["original_url"] == "https://facebook.com/"
  assert data["short_code"]
  assert len(data["short_code"]) == 6 
  assert data["click_count"] == 0
  assert data["expires_at"] == None

