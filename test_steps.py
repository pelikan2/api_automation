import requests #to request https endpoint
import endpoint as ENDPOINT


def test_can_call_endpoint():
    response = requests.get(ENDPOINT.User_ENDPOINT + "/user1")
    assert response.status_code == 200 # check if status code is 200

def test_can_create_user():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200

    data = create_user_response.json()

    status = data["code"]
    get_response = create_user_response.status_code

    assert get_response == status
    username = payload["username"]
    get_user_response = ENDPOINT.get_user(username)

    get_user_response = get_user_response.json()
    assert get_user_response["firstName"] == payload["firstName"]
    assert get_user_response["username"] == payload["username"]

def test_can_update_user():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    username = payload["username"]

    new_payload = {
        "id": 0,
        "username": username,
        "firstName": 'Ferkoooo',
        "lastName": "Mrkvickaaaa",
        "email": "ferko.mrkvicka@gmail.com",
        "password": "1234",
        "phone": "421949888555",
        "userStatus": 0,
    }
    update_user_response = ENDPOINT.update_user(username, new_payload)
    assert update_user_response.status_code == 200

    get_user_response = ENDPOINT.get_user(username)
    assert get_user_response.status_code == 200
    get_user_data = get_user_response.json()
    assert get_user_data["firstName"] == new_payload["firstName"]
    assert get_user_data["username"] == new_payload["username"]

def test_can_delete_user():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    username = payload["username"]

    delete_user_response = ENDPOINT.delete_user(username)
    assert delete_user_response.status_code == 200

    get_user_response = ENDPOINT.get_user(username)
    assert get_user_response.status_code == 404

def test_can_login_user():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    data = create_user_response.json()

    status = data["code"]
    get_response = create_user_response.status_code
    assert get_response == status

    get_user_response = ENDPOINT.login_user(user_name=payload["username"], password=payload["password"])
    assert get_user_response.status_code == 200

def test_can_create_list():
    payload = ENDPOINT.create_list_users()
    create_user_response = ENDPOINT.create_list(payload)
    assert create_user_response.status_code == 200

def test_can_order():
    payload = ENDPOINT.create_order()
    create_order_response = ENDPOINT.store_order(payload)
    assert create_order_response.status_code == 200

    get_order_data = create_order_response.json()
    assert get_order_data["petId"] == payload["petId"]
    assert get_order_data["quantity"] == payload["quantity"]

    orderId = payload["id"]
    get_order_response = ENDPOINT.get_order(orderId)

    get_order_response = get_order_response.json()
    assert get_order_response["petId"] == payload["petId"]
    assert get_order_response["quantity"] == payload["quantity"]

def test_can_delete_order():
    payload = ENDPOINT.create_order()
    create_order_response = ENDPOINT.store_order(payload)
    assert create_order_response.status_code == 200
    id = payload["id"]

    delete_order_response = ENDPOINT.delete_user(id)
    assert delete_order_response.status_code == 200

    get_order_response = ENDPOINT.get_order(id)
    assert get_order_response.status_code == 404

def test_can_check_inventory():
    get_inventory_response = ENDPOINT.get_inventory()
    assert get_inventory_response.status_code == 200