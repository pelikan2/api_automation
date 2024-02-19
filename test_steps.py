import pytest #import kniznice pytest
import requests  # to request https endpoint
import allure # importuje kniznicu, ktora sluzi na vytvaranie test reportov
import endpoint as ENDPOINT # import nasho modulu endpoint, ktory je pomenovany ako ENDPOINT


#user tag, tag sa pouziva na zgrupenie urcitej casti testov
@pytest.mark.user
# test sa skontrolovanie endpointu s requestom get
def test_can_call_endpoint():
    response = requests.get(ENDPOINT.User_ENDPOINT + "/user1")
    assert response.status_code == 200  # skontroluje, ci je status code 200, tzn. ok


@pytest.mark.user
@allure.feature("user")
@allure.severity(allure.severity_level.BLOCKER)
# test na vytvorenie noveho uzivatela
def test_can_create_user():
    payload = ENDPOINT.new_user_payload() #do pemennej payload ukladam slovnik, ktory som si vytvoril v module endpoint
    create_user_response = ENDPOINT.create_user(payload)  # vytvorenie uzivatela pomocou funkcie z modulu endpoint
    assert create_user_response.status_code == 200  # skontroluje, ci status kod tejto operiacie je 200

    data = create_user_response.json()  #ukladanie vystupu z predoslej operacie do premennej data

    status = data["code"]  # ukladanie hodnoty "code" zo slovnika data do premennej status
    get_response = create_user_response.status_code # ukladanie status_code do premennej get_response

    assert get_response == status # kontroluje, ci hodnoty z predchadzajucich dvoch premennych sa rovnaju
    username = payload["username"] # ukladanie hodnoty username do premennej username
    get_user_response = ENDPOINT.get_user(username) # pouzitie funkcie get_user so vstupnym parametrom username z predchadzajucej premennej
    # dostanem novo vytvoreneho uzivatela

    get_user_response = get_user_response.json() # ukladanie odpovede z volania API do json formatu
    assert get_user_response["firstName"] == payload["firstName"] # kontrola, ci sa hodnota "firstName" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel
    assert get_user_response["username"] == payload["username"] # kontrola, ci sa hodnota "username" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel


@pytest.mark.user
@allure.feature("user")
@allure.severity(allure.severity_level.NORMAL)
# test na zmenu noveho uzivatela
def test_can_update_user():
    # vytvorenie noveho uzivatela a kontrola status_code
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    username = payload["username"]
 # vytvorenie noveho payloadu prostrednictvojm slovnika.
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
    # aktualizacia uzivatela pomocou novovytvoreneho payloadu, kontrola status_code
    update_user_response = ENDPOINT.update_user(username, new_payload)
    assert update_user_response.status_code == 200

    # volanie funkcie get_user na kontrolu zmien z predoslej operacie a kontrola status_code
    get_user_response = ENDPOINT.get_user(username)
    assert get_user_response.status_code == 200
    get_user_data = get_user_response.json()

    #kontrola danych hodnot, ktore by sa mali zmenit, ak doslo k aktualizacii
    assert get_user_data["firstName"] == new_payload["firstName"]
    assert get_user_data["username"] == new_payload["username"]


@pytest.mark.user
@allure.feature("user")
@allure.severity(allure.severity_level.NORMAL)
#test na vymazanie noveho uzivatela
def test_can_delete_user():

    # vytvorenie noveho uzivatela a kontrola status_code
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    username = payload["username"]

    # pouzite api delete na vymazanie uzivatela a kontrola status_code
    delete_user_response = ENDPOINT.delete_user(username)
    assert delete_user_response.status_code == 200

    # kontrola, ci je dany uzivatel vymazany, kontrola zodpovedajuceho status_code (404, not found)
    get_user_response = ENDPOINT.get_user(username)
    assert get_user_response.status_code == 404


@pytest.mark.user
@allure.feature("user")
@allure.severity(allure.severity_level.BLOCKER)
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
    assert get_user_response_logout.status_code == 200


@pytest.mark.user
@allure.feature("user")
@allure.severity(allure.severity_level.BLOCKER)
def test_login():
    payload = ENDPOINT.new_user_payload()
    create_user_response = ENDPOINT.create_user(payload)
    assert create_user_response.status_code == 200
    date = create_user_response.json()

    status = date["code"]
    get_response = create_user_response.status_code
    assert get_response == status
    # pouzitie login_user funkcie z modulu endpoint s pouzitim pametrov z payloadu
    get_user_response = ENDPOINT.login_user(username=payload["username"], password=payload["password"])
    assert get_user_response.status_code == 200


@pytest.mark.user
@allure.feature("user")
@allure.severity(allure.severity_level.CRITICAL)
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


@pytest.mark.user
@allure.feature("user")
@allure.severity(allure.severity_level.MINOR)
def test_can_create_list():
    payload = ENDPOINT.create_list_users()
    create_user_response = ENDPOINT.create_list(payload)
    assert create_user_response.status_code == 200


# store tag
@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.MINOR)
def test_store_order():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.NORMAL)
def test_store_order_id():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200

    response_json = response_store.json()
    store_order = ENDPOINT.store_order_id(response_json["id"])
    assert store_order.status_code == 200


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.MINOR)
def test_store_order_id_404():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200

    store_order = ENDPOINT.store_order_id("9")
    assert store_order.status_code == 404


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.BLOCKER)
def test_store_delete_order_id():
    payload = ENDPOINT.new_store_payload()
    response_store = ENDPOINT.store_order(payload)
    assert response_store.status_code == 200

    response_json = response_store.json()
    store_order = ENDPOINT.store_order_id(response_json["id"])
    assert store_order.status_code == 200

    delete = ENDPOINT.store_delete_order_id(response_json["id"])
    assert delete.status_code == 200


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.CRITICAL)
def test_store_delete_order_id_404():
    delete = ENDPOINT.store_delete_order_id("9")
    assert delete.status_code == 404


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.NORMAL)
def test_inventory():
    response = ENDPOINT.store_get_inventory()
    assert response.status_code == 200

# pet tag
@pytest.mark.pet
@allure.feature("pet")
@allure.severity(allure.severity_level.BLOCKER)
def test_create_pet():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200


@pytest.mark.pet
@allure.feature("pet")
@allure.severity(allure.severity_level.CRITICAL)
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


@pytest.mark.pet
@allure.feature("pet")
@allure.severity(allure.severity_level.NORMAL)
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


@pytest.mark.pet
@allure.feature("pet")
@allure.severity(allure.severity_level.MINOR)
def test_find_pet_id():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200
    create_response = response_pet.json()

    find_pet = ENDPOINT.find_pet_id(create_response["id"])
    assert find_pet.status_code == 200


@pytest.mark.pet
@allure.feature("pet")
@allure.severity(allure.severity_level.MINOR)
def test_find_pet_id_404():
    find_pet = ENDPOINT.find_pet_id(15)
    assert find_pet.status_code == 404


@pytest.mark.pet
@allure.feature("pet")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_id():
    payload = ENDPOINT.new_pet_payload()
    response_pet = ENDPOINT.pet_create(payload)
    assert response_pet.status_code == 200
    create_response = response_pet.json()

    find_pet = ENDPOINT.delete_pet_id(create_response["id"])
    assert find_pet.status_code == 200


@pytest.mark.pet
@allure.feature("pet")
@allure.severity(allure.severity_level.MINOR)
def test_delete_pet_id_404():
    find_pet = ENDPOINT.delete_pet_id(150)
    assert find_pet.status_code == 404


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.CRITICAL)
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


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.BLOCKER)
def test_can_delete_order():
    payload = ENDPOINT.create_order()
    create_order_response = ENDPOINT.store_order(payload)
    assert create_order_response.status_code == 200
    id = payload["id"]

    delete_order_response = ENDPOINT.delete_user(id)
    assert delete_order_response.status_code == 200

    get_order_response = ENDPOINT.get_order(id)
    assert get_order_response.status_code == 404


@pytest.mark.store
@allure.feature("store")
@allure.severity(allure.severity_level.MINOR)
def test_can_check_inventory():
    get_inventory_response = ENDPOINT.get_inventory()
    assert get_inventory_response.status_code == 200