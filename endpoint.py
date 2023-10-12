import requests

User_ENDPOINT = "https://petstore.swagger.io/v2/user"

def create_user(payload):
    return requests.post(User_ENDPOINT, json=payload)

def update_user(user_name, payload):
    return requests.put(User_ENDPOINT + f"/{user_name}", json=payload)

def get_user(user_name):
    return requests.get(User_ENDPOINT + f"/{user_name}")

def delete_user(user_name):
    return requests.delete(User_ENDPOINT + f"/{user_name}")

def new_user_payload():
    user_name = "user1"
    return {
        "id": 0,
        "username": user_name,
        "firstName": 'Ferko',
        "lastName": "Mrkvicka",
        "email": "ferko.mrkvicka@gmail.com",
        "password": "1234",
        "phone": "421949888555",
        "userStatus": 0,
    }