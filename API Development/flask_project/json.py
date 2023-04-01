import requests

# Register a user
response = requests.post('http://localhost:5000/register', json={'username': 'john', 'password': 'doe'})
print(response.status_code) # 201

# Login with the registered user
response = requests.post('http://localhost:5000/login', json={'username': 'john', 'password': 'doe'})
access_token = response.json()['access_token']
print(response.status_code) # 200

# Create a TA
ta_data = {
    'native_english_speaker': True,
    'course_instructor': 'Jane Smith',
    'course': 'CS101',
    'semester': 'Fall 2022',
    'class_size': 50,
    'performance_score': 8.5
}
response = requests.post('http://localhost:5000/api/tas', json=ta_data, headers={'Authorization': f'Bearer {access_token}'})
print(response.status_code) # 201

# Get the created TA
response = requests.get('http://localhost:5000/api/tas/1', headers={'Authorization': f'Bearer {access_token}'})
print(response.status_code) # 200
print(response.json()) # {'id': 1, 'native_english_speaker': True, 'course_instructor': 'Jane Smith', 'course': 'CS101', 'semester': 'Fall 2022', 'class_size': 50, 'performance_score': 8.5}

# Get all TAs
response = requests.get('http://localhost:5000/api/tas', headers={'Authorization': f'Bearer {access_token}'})
print(response.status_code) # 200
print(response.json()) # [{'id': 1, 'native_english_speaker': True, 'course_instructor': 'Jane Smith', 'course': 'CS101', 'semester': 'Fall 2022', 'class_size': 50, 'performance_score': 8.5}]

# Update the created TA
ta_data = {
    'native_english_speaker': False,
    'course_instructor': 'John Doe',
    'course': 'CS102',
    'semester': 'Spring 2023',
    'class_size': 40,
    'performance_score': 7.5
}
response = requests.put('http://localhost:5000/api/tas/1', json=ta_data, headers={'Authorization': f'Bearer {access_token}'})
print(response.status_code) # 200

# Delete the created TA
response = requests.delete('http://localhost:5000/api/tas/1', headers={'Authorization': f'Bearer {access_token}'})
print(response.status_code) # 200
