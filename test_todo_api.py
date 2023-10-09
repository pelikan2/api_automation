import requests #to request https endpoint
import uuid # unigue identifier



ENDPOINT = "https://todo.pixegami.io"

response = requests.get(ENDPOINT)
print(response)

data = response.json()
print(data)

status_code = response.status_code
print(status_code)


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200 # check if status code is 200

def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200
    get_task_response = get_task_response.json()
    assert get_task_response["content"] == payload["content"] # na fail staci napisat nejaky iny string
    assert get_task_response["user_id"] == payload["user_id"]
    print(get_task_response)

def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
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

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_can_list_tasks():
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    user_id = payload["user_id"]
    list_task_reponse = list_tasks(user_id)
    assert list_task_reponse.status_code == 200
    data = list_task_reponse.json()

    tasks = data["tasks"]
    assert len(tasks) == n

def test_can_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404

def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks{user_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task{task_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "task_id": "test_task_id",  # nemusime, lebo je generovany
        "is_done": False,
    }