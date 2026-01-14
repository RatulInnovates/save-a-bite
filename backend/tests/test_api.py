from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_create_listing():
    # register
    r = client.post('/api/users/register', json={"name":"T Test","email":"test@example.com","password":"p","user_type":"Donor"})
    assert r.status_code == 200
    data = r.json()
    assert data['email'] == 'test@example.com'

    # create listing
    # create donor profile (lightweight: assume donor_id 1 exists from seed)
    r2 = client.post('/api/listings/', json={"donor_id":1, "food_details":"Test food", "quantity":"5 kg"})
    assert r2.status_code in (200,201)
    data2 = r2.json()
    assert 'listing_id' in data2
