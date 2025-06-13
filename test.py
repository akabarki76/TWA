import pytest
import time

@pytest.fixture
def vulnerable_client():
    from code import app
    app.config['TESTING'] = True
    return app.test_client()

def test_timing_leak(vulnerable_client):
    valid_times = []
    invalid_times = []
    
    for _ in range(10):
        start = time.time()
        vulnerable_client.post('/auth', json={"user_id": 1001, "pin": "wrong"})
        valid_times.append(time.time() - start)
        
        start = time.time()
        vulnerable_client.post('/auth', json={"user_id": 9999, "pin": "wrong"})
        invalid_times.append(time.time() - start)
    
    assert statistics.mean(valid_times) > statistics.mean(invalid_times) * 2
