import requests
import json

# Define the URL and the JSON payload
url = 'https://lenskits.polynomial.ai/entity_model/predict'  # Replace with your secure link
payload = {
    "session_id": "",
    "model_id": "propex_properties",
    "query": "what is the address of Colive Paradise",
    "threshold": 80.0,
    "query_type": "NORMAL"
}

# Convert the payload to a JSON string
payload_json = json.dumps(payload)

# Set the headers for the request
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, headers=headers, data=payload_json)

# Check the response
if response.status_code == 200:
    print("Success:")
    print(response.json())
else:
    print(f"Failed with status code {response.status_code}:")
    print(response.text)
