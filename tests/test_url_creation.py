def test_url_creation(client):
  response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com"
    }
  )


  assert response.status_code == 201

  data = response.json()

  assert data["original_url"] == "https://facebook.com/"
  assert data["short_code"]
  assert len(data["short_code"]) == 6 
  assert data["click_count"] == 0
  assert data["expires_at"] == None

def test_redirecting_url(client): 
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com"
    }
  )

  assert create_response.status_code == 201

  create_response_data = create_response.json() 

  assert create_response_data["original_url"] == "https://facebook.com/"
  assert create_response_data["short_code"]
  assert len(create_response_data["short_code"]) == 6 
  assert create_response_data["click_count"] == 0
  assert create_response_data["expires_at"] == None

  create_response_short_code = create_response_data["short_code"]

  response = client.get(
    f"/{create_response_short_code}",
    follow_redirects=False
  )

  assert response.status_code == 307

def test_getting_nonexistent_url(client):
  response = client.get(
    "/urls/AKRP35"
  )

  assert response.status_code == 404

def test_missing_url(client):
  response = client.post(
    "/urls",
    json={}
  )
  
  assert response.status_code == 422