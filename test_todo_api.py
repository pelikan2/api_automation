import requests #to request https endpoint
import uuid # unigue identifier



ENDPOINT = "https://petstore.swagger.io/v2/user"

response = requests.get(ENDPOINT + "/user1")
print(response)

data = response.json()
print(data)

status_code = response.status_code
print(status_code)


def test_can_call_endpoint():
    response = requests.get(ENDPOINT + "/user1")
    assert response.status_code == 200 # check if status code is 200

def test_can_create_user():
    payload = new_user_payload()
    create_user_response = create_user(payload)
    assert create_user_response.status_code == 200

    data = create_user_response.json()
    print(data)

    user_name = data["user1"]["username"]
    get_user_response = get_user(user_name)

    assert get_user_response.status_code == 200
    get_user_response = get_user_response.json()
    assert get_user_response["firstName"] == payload["firstName"] # na fail staci napisat nejaky iny string
    assert get_user_response["username"] == payload["username"]
    print(get_user_response)

def test_can_update_task():
    payload = new_user_payload()
    create_task_response = create_user(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    new_payload = {
        "content": "my updated content",
        "user_id": payload["user_id"],
        "task_id": task_id,  # nemusime, lebo je generovany
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    get_task_response = get_user(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_can_list_tasks():
    n = 3
    payload = new_user_payload()
    for _ in range(n):
        create_task_response = create_user(payload)
        assert create_task_response.status_code == 200
    user_id = payload["user_id"]
    list_task_reponse = list_tasks(user_id)
    assert list_task_reponse.status_code == 200
    data = list_task_reponse.json()

    tasks = data["tasks"]
    assert len(tasks) == n

def test_can_delete_task():
    payload = new_user_payload()
    create_task_response = create_user(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_user(task_id)
    assert get_task_response.status_code == 404

def create_user(payload):
    return requests.post(ENDPOINT, json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_user(user_name):
    return requests.get(ENDPOINT + f"/{user_name}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks{user_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task{task_id}")

def new_user_payload():
    user_name = "user1"
    return {
        "username": user_name,
        "firstName": 'Ferko',
        "lastName": "Mrkvicka",  # nemusime, lebo je generovany
        "email": "ferko.mrkvicka@gmail.com",
        "password": "1234",
        "phone": "421949888555",
        "userStatus": 0,
    }