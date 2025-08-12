import requests

base_url = "http://0.0.0.0:8000"

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "a",
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "tickets_wanted": 1,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "a",
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "tickets_wanted": 1,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "b",
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "tickets_wanted": 3,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "c",
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "tickets_wanted": 2,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "d",
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "tickets_wanted": 5,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "e",
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "tickets_wanted": 4,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "f",
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "tickets_wanted": 4,
    }
)
print(response.content)

response = requests.put(
    url=f"{base_url}/user/leave-list",
    json={
        "user_id": "c",
        "offer_id": "off_001",
        "representation_id": "rep_001",
    }
)
print(response.content)

response = requests.get(
    url=f"{base_url}/user/get-status",
    params={
        "user_id": "e",
        "offer_id": "off_001",
        "representation_id": "rep_001"
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "b",
        "offer_id": "off_001",
        "representation_id": "rep_002",
        "tickets_wanted": 2,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "b",
        "offer_id": "off_001",
        "representation_id": "rep_003",
        "tickets_wanted": 2,
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/user/join-list",
    json={
        "user_id": "a",
        "offer_id": "off_001",
        "representation_id": "rep_002",
        "tickets_wanted": 2,
    }
)
print(response.content)

response = requests.get(
    url=f"{base_url}/user/get-all-status",
    params={
        "user_id": "a",
    }
)
print(response.content)

response = requests.get(
    url=f"{base_url}/user/get-status",
    params={
        "user_id": "a",
        "offer_id": "off_001",
        "representation_id": "rep_001"
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/organizer/get-waiting-lists",
    json={
        "offer_ids": ["off_001"],
        "representation_ids": ["rep_001", "rep_002"],
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/organizer/get-waiting-lists",
    json={
        "user_ids": ["a", "b"],
        "offer_ids": ["off_001"],
        "representation_ids": ["rep_001"],
    }
)
print(response.content)

response = requests.put(
    url=f"{base_url}/organizer/add-stock",
    json={
        "offer_id": "off_001",
        "representation_id": "rep_001",
        "stock_amount": 10
    }
)
print(response.content)

response = requests.post(
    url=f"{base_url}/organizer/buy-tickets",
    json={
        "user_id": "a",
        "offer_id": "off_001",
        "representation_id": "rep_001",
    }
)
print(response.content)

