from datetime import datetime, timezone, timedelta

from models.url import Url

# ----------   TEST   URL   CREATION   ----------

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

def test_generated_short_code(client):
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com/"
    }
  )

  short_code = create_response.json()["short_code"]

  short_url_response = client.get(
    f"/{short_code}",
    follow_redirects=False
  )

  assert short_url_response is not None 
  assert short_url_response.status_code == 307
  assert short_url_response.headers["location"] == "https://facebook.com/"

def test_unique_short_code(client): 
  response1 = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com/"
    }
  )

  response2 = client.post(
    "/urls",
    json={
      "original_url": "https://google.com"
    }
  )

  data1 = response1.json()
  data2 = response2.json()



  assert response1.status_code == 201
  assert response2.status_code == 201

  assert data1["short_code"] != data2["short_code"]


# ----------   TEST   REDIRECTING   ----------

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
  assert response.headers["location"] == "https://facebook.com/"

def test_nonexistent_short_code_redirect(client):
  response = client.get(
      "/AK5RP3",
      follow_redirects=False
  )

  assert response.status_code == 404

def test_inactive_url(client, db): 
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com"
    }
  )

  assert create_response.status_code == 201 

  short_code = create_response.json()["short_code"]

  url = db.query(Url).filter(Url.short_code == short_code).first()

  url.is_active = False
  db.commit() 

  response = client.get(
    f"/{short_code}"
  )

  assert response.status_code == 404
  assert response.json()["detail"] == "URL is inactive"

def test_expired_url(client, db): 
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com"
    }
  )

  assert create_response.status_code == 201 

  response_data = create_response.json()

  short_code = response_data["short_code"]

  url = db.query(Url).filter(Url.short_code == short_code).first()

  url.expires_at = datetime.now(timezone.utc) - timedelta(days=10)
  db.commit() 

  response = client.get(
    f"/{short_code}"
  )

  assert response.status_code == 404
  assert response.json()["detail"] == "URL is expired"

def test_click_count_increases(client, db):
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com/"
    }
  )
  
  assert create_response.status_code == 201

  data = create_response.json()
  short_code = data["short_code"]

  url = db.query(Url).filter(Url.short_code == short_code).first()

  response1 = client.get(
    f"/{short_code}",
    follow_redirects=False
  )
  
  assert response1.status_code == 307
  assert url.click_count == 1

  response2 = client.get(
    f"/{short_code}",
    follow_redirects=False
  )
  
  assert response2.status_code == 307
  assert url.click_count == 2


# ----------   TEST   URL MANAGEMENT   ----------

def test_retrieving_url(client, db):
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com/"
    }
  )
  
  assert create_response.status_code == 201
  
  data = create_response.json()
  short_code = data["short_code"]

  url = db.query(Url).filter(Url.short_code == short_code).first() 

  assert url.original_url == "https://facebook.com/"

def test_updating_url(client, db):
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com/"
    }
  )
  
  assert create_response.status_code == 201
  
  data = create_response.json()
  short_code = data["short_code"]  

  url = db.query(Url).filter(Url.short_code == short_code).first()
  
  assert url.original_url == "https://facebook.com/"

  update_response = client.put(
    f"/urls/{short_code}",
    json={
      "original_url": "https://learnx.ge/"
    }
  )

  print(update_response.json())

  assert update_response.status_code == 200

  updated_data = update_response.json()
  updated_short_code = updated_data["short_code"]

  updated_url = db.query(Url).filter(Url.short_code == updated_short_code).first() 

  assert updated_url.original_url == "https://learnx.ge/"

def test_deleting_url(client):
  create_response = client.post(
    "/urls",
    json={
      "original_url": "https://facebook.com/"
    }
  )
  
  assert create_response.status_code == 201
  
  data = create_response.json()
  short_code = data["short_code"]  

  delete_response = client.delete(
    f"/urls/{short_code}"
  )
  
  assert delete_response.status_code == 204 

  response = client.get(
    f"/urls/{short_code}"
  )

  assert response.status_code == 404 
  assert response.json()["detail"] == "URL not found"