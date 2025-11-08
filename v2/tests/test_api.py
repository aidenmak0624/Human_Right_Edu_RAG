import requests

# Test chat endpoint
response = requests.post('http://localhost:5050/api/chat', json={
    'query': 'What is the CRC?',
    'topic': 'childrens_rights'
})

print(response.json())