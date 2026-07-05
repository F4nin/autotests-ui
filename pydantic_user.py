from pydantic import BaseModel, ValidationError


class User(BaseModel):
    model_config = dict(strict=True)

    id: int
    name: str
    email: str
    is_active: bool = True


user_first = {
    'id': 12,
    'name': 'BobaFet',
    'email': 12
}

try:
    user = User(**user_first)
except ValidationError as e:
    print(f'Ошибка влидации {e}')