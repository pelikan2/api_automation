import endpoint as ENDPOINT # import nasho modulu endpoint, ktory je pomenovany ako ENDPOINT

def test_can_create_user_template():
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
    assert get_user_response["id"] == payload["id"] # kontrola, ci sa hodnota "id" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel
    assert get_user_response["lastName"] == payload["lastName"] # kontrola, ci sa hodnota "lastName" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel
    assert get_user_response["email"] == payload["email"] # kontrola, ci sa email "lastName" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel
    assert get_user_response["password"] == payload["password"] # kontrola, ci sa email "password" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel
    assert get_user_response["phone"] == payload["phone"] # kontrola, ci sa email "phone" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel
    assert get_user_response["userStatus"] == payload["userStatus"] # kontrola, ci sa email "userStatus" z get_user = s hodnotou,
    # ktora sa pouzila pri vytvoreni noveho uzivatel