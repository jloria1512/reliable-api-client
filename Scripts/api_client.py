import requests
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str


def get_user(user_id: int, timeout: float = 10.0) -> User:
    get_user_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = requests.get(get_user_url, timeout=timeout)
    response.raise_for_status()
    user = User(**response.json())
    return user

if __name__ == "__main__":
    user = get_user(4)
    print(user)