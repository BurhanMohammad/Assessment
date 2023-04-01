import json
from app import app, db, TA, User

def test_create_user():
    client = app.test_client()
    response = client.post('/register', json={'username': 'user1', 'password': 'pass1'})
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_create_user_with_existing_username():
    client = app.test_client()
    response = client.post('/register', json={'username': 'user1', 'password': 'pass1'})
    assert response.status_code == 409
    assert b'Username already exists' in response.data

def test_login():
    client = app.test_client()
    response = client.post('/login', json={'username': 'user1', 'password': 'pass1'})
    assert response.status_code == 200
    assert b'access_token' in response.data

def test_login_with_invalid_credentials():
    client = app.test_client()
    response = client.post('/login', json={'username': 'user1', 'password': 'wrong_password'})
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data

def test_create_ta():
    client = app.test_client()
    headers = {'Authorization': 'Bearer ' + get_access_token()}
    response = client.post('/api/tas', json={
        'native_english_speaker': True,
        'course_instructor': 'John Smith',
        'course': 'CS101',
        'semester': 'Fall 2022',
        'class_size': 50,
        'performance_score': 4.5,
    }, headers=headers)
    assert response.status_code == 201
    assert b'TA created successfully' in response.data

def test_get_ta():
    client = app.test_client()
    headers = {'Authorization': 'Bearer ' + get_access_token()}
    response = client.get('/api/tas/1', headers=headers)
    assert response.status_code == 200
    assert b'John Smith' in response.data

def test_get_nonexistent_ta():
    client = app.test_client()
    headers = {'Authorization': 'Bearer ' + get_access_token()}
    response = client.get('/api/tas/100', headers=headers)
    assert response.status_code == 404
    assert b'TA not found' in response.data

def test_get_tas():
    client = app.test_client()
    headers = {'Authorization': 'Bearer ' + get_access_token()}
    response = client.get('/api/tas', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0

def test_update_ta():
    client = app.test_client()
    headers = {'Authorization': 'Bearer ' + get_access_token()}
    response = client.put('/api/tas/1', json={
        'native_english_speaker': False,
        'course_instructor': 'Jane Doe',
        'course': 'CS102',
        'semester': 'Spring 2023',
        'class_size': 60,
        'performance_score': 4.8,
    }, headers=headers)
    assert response.status_code == 200
    assert b'TA updated successfully' in response.data

def test_delete_ta():
    client = app.test_client()
    headers = {'Authorization': 'Bearer ' + get_access_token()}
    response = client.delete('/api/tas/1', headers=headers)
    assert response.status_code == 200
    assert b'TA deleted successfully' in response.data

def get_access_token():
    client = app.test_client()
    response = client.post('/login', json={'username': 'admin', 'password': 'admin'})
    data = json.loads(response.data)
    return data['access_token']

