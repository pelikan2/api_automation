import requests #to request https endpoint
import endpoint as ENDPOINT
import uuid # unigue identifier


def test_can_call_endpoint():
    response = requests.get(ENDPOINT.User_ENDPOINT + "/user3")
    assert response.status_code == 200 # check if status code is 200

def test_can_create_user():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200

    data = create_user_response.json()
    print(data)

    status = data["code"]
    get_response = create_user_response.status_code

    assert get_response == status
    username = payload["username"]
    get_user_response = ENDPOINT.get_user(username)

    get_user_response = get_user_response.json()
    assert get_user_response["firstName"] == payload["firstName"]
    assert get_user_response["username"] == payload["username"]
    print(get_user_response)

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
    print(username)

    delete_user_response = ENDPOINT.delete_user(username)
    assert delete_user_response.status_code == 200

    get_user_response = ENDPOINT.get_user(username)
    assert get_user_response.status_code == 404


def test_can_logout():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    date = create_user_response.json()

    status = date["code"]
    get_response = create_user_response.status_code
    assert get_response == status

    get_user_response = ENDPOINT.login_user(username=payload["username"], password=payload["password"])
    assert get_user_response.status_code == 200

    get_user_response_logout = ENDPOINT.get_logout()

    # get_user_logout = get_user_response_logout.json()
    assert get_user_response_logout.status_code == 200


def test_login():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    date = create_user_response.json()

    status = date["code"]
    get_response = create_user_response.status_code
    assert get_response == status

    get_user_response = ENDPOINT.login_user(username=payload["username"], password=payload["password"])
    assert get_user_response.status_code == 200


def test_can_create_list():
    payload = ENDPOINT.create_list_users()
    create_user_response = ENDPOINT.create_list(payload)
    assert create_user_response.status_code == 200


def test_store_order():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200


def test_store_order_id():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200

    response_json = response_store.json()
    store_order = ENDPOINT.store_order_id(response_json["id"])
    assert store_order.status_code == 200


def test_store_order_id_404():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200

    store_order = ENDPOINT.store_order_id("9")
    assert store_order.status_code == 404


def test_store_delete_order_id():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200

    response_json = response_store.json()
    store_order = ENDPOINT.store_order_id(response_json["id"])
    assert store_order.status_code == 200

    delete = ENDPOINT.store_delete_order_id(response_json["id"])
    assert delete.status_code == 200


def test_store_delete_order_id_404():
    delete = ENDPOINT.store_delete_order_id("9")
    assert delete.status_code == 404


def test_inventory():
    response = ENDPOINT.store_get_inventory()
    assert response.status_code == 200


def test_create_pet():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200


def test_update_pet():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200
    create_response = response_pet.json()

    payload = ENDPOINT.update_pet_payload()
    response_pet = ENDPOINT.pet_update(payload)
    assert response_pet.status_code == 200
    update_response = response_pet.json()

    assert create_response["name"] != update_response["name"]
    assert create_response["id"] == update_response["id"]


def test_update_pet_404():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200
    create_response = response_pet.json()

    payload = ENDPOINT.update2_pet_payload()
    response_pet = ENDPOINT.pet_update(payload)
    assert response_pet.status_code == 404
    update_response = response_pet.json()

    assert create_response["name"] != update_response["name"]
    assert create_response["id"] != update_response["id"]

    payload = ENDPOINT.update_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 404


def test_find_pet_id():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200
    create_response = response_pet.json()

    find_pet = ENDPOINT.find_pet_id(create_response["id"])
    assert find_pet.status_code == 200


def test_find_pet_id_404():
    find_pet = ENDPOINT.find_pet_id(15)
    assert find_pet.status_code == 404


def test_delete_id():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200
    create_response = response_pet.json()

    find_pet = ENDPOINT.delete_pet_id(create_response["id"])
    assert find_pet.status_code == 200


def test_delete_pet_id_404():
    find_pet = ENDPOINT.delete_pet_id(150)
    assert find_pet.status_code == 404