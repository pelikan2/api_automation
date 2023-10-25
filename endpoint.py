import requests

User_ENDPOINT = "https://petstore.swagger.io/v2/user"
Store_ENDPOINT = "https://petstore.swagger.io/v2/store"

def create_user(payload):
    return requests.post(User_ENDPOINT, json=payload)

def update_user(user_name, payload):
    return requests.put(User_ENDPOINT + f"/{user_name}", json=payload)

def get_user(user_name):
    return requests.get(User_ENDPOINT + f"/{user_name}")

def delete_user(user_name):
    return requests.delete(User_ENDPOINT + f"/{user_name}")

def login_user(user_name, password):
    return requests.get(User_ENDPOINT + "/login")

def create_list(payload):
    return requests.post(User_ENDPOINT + "/createWithList", json=payload)

def create_list_users():
    dict = [{
        "id": 1,
        "username": "user1",
        "firstName": 'Ferko',
        "lastName": "Mrkvicka",
        "email": "ferko.mrkvicka@gmail.com",
        "password": "1234",
        "phone": "421949888555",
        "userStatus": 0
    },
        {
            "id": 2,
            "username": "user2",
            "firstName": 'Fer',
            "lastName": "Mrk",
            "email": "fer.mrk@gmail.com",
            "password": "4321",
            "phone": "421949888333",
            "userStatus": 0
        }
    ]
    return dict
def new_user_payload():
    user_name = "user3"
    return {
        "id": 1,
        "username": user_name,
        "firstName": 'Ferko',
        "lastName": "Mrkvicka",
        "email": "ferko.mrkvicka@gmail.com",
        "password": "1234",
        "phone": "421949888555",
        "userStatus": 0,
    }

# store endpoint

def create_order():
    return {
  "id": 1,
  "petId": 1,
  "quantity": 2,
  "shipDate": "2023-10-25T09:39:01.330Z",
  "status": "placed",
  "complete": True
}

def store_order(payload):
    return requests.post(Store_ENDPOINT + "/order", json=payload)

def get_order(orderId):
    return requests.get(Store_ENDPOINT + f"/order/{orderId}")

def delete_order(orderId):
    return requests.delete(Store_ENDPOINT + f"/order/{orderId}")

def get_inventory():
    return requests.get(Store_ENDPOINT + "/inventory")