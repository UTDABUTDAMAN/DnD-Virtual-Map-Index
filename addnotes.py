import requests

# Base URL of your local Flask app
url = 'http://127.0.0.1:5000/notes'

# Data to send (if your Flask app expects request.json)
payload = {'location_id': 1,
           'notes': 'Whatever'}

# Sending a POST request
response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())