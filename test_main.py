from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_members():
    response = client.get('/member/')
    assert response.status_code ==200
    
def get_memberdetails():
    response = client.get('/get/member/1')
    assert response.status_code == 200