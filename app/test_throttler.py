

import pytest
from fastapi.testclient import TestClient


from .app import app
import time


client = TestClient(app)




"""
    Initiate startup event for app to create redis db connection
"""
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c




def test_throttler(client):
    '''
    Test 1: 
    
    Basic functionality testing with a simple echo 
    
    '''

    response = client.post("/echo",json={"data": 1})
    assert response.status_code == 200
    assert response.json() == {"data": 1}
    '''
    Test 2: 
    
    Test  SET & GET /rate 
    
    '''

    response = client.get("/rate")
    assert response.json() == {"request_rate": 5}
    response2 = client.post("/rate", json = {"request_rate": 10})
    assert response2.status_code == 200
    response3 = client.get("/rate")
    assert response3.status_code == 200
    assert response3.json() == {"request_rate": 10}

    '''
    Test 3: 
    
    Test throttling middleware, time.sleep[65] assures the counter resets.
    Since request_rate = 10, 11th try should fail with a 429
    '''


    time.sleep(65)
    response_list = []
    for i in range(11) :
        response_list.append(client.post("/echo",json={"data": 1}))
    for j in range(10):
        assert response_list[j].status_code == 200
        assert response_list[j].json() == {"data": 1}
    
    assert response_list[10].status_code == 429

'''

@pytest.mark.skip(reason="no way of currently testing this")
def test2_database(client):
    response = client.get("/rate")
    assert response.json() == {"request_rate": 5}
    response2 = client.post("/rate", json = {"request_rate": 10})
    assert response2.status_code == 200
    response3 = client.get("/rate")
    assert response3.status_code == 200
    assert response3.json() == {"request_rate": 10}

@pytest.mark.skip(reason="no way of currently testing this")
def test3_throttler(client):
    time.sleep(65)
    response_list = []
    for i in range(6) :
        response_list.append(client.post("/echo",json={"data": 1}))
    for j in range(5):
        assert response_list[j].status_code == 200
        assert response_list[j].json() == {"data": 1}
    
    assert response_list[5].status_code == 428

'''
