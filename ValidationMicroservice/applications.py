import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, EmailStr, field_validator


class Application(BaseModel):
    timestamp: str = Field(..., description="Временная метка заявки")
    full_name: str = Field(..., min_length=1, max_length=100, description="Полное имя заявителя")
    user_id: str = Field(..., min_length=1, max_length=50, description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(..., description="Электронная почта заявителя")
    phone_number: str = Field(..., description="Номер телефона заявителя")
    address: str = Field(..., min_length=1, max_length=255, description="Адрес заявителя")
    date_of_birth: str = Field(..., description="Дата рождения заявителя")
    gender: str = Field(..., description="Пол заявителя")
    event_description: str = Field(..., min_length=1, max_length=500, description="Описание события")

    @field_validator("address")
    def validate_address(cls, value):
        address_regex = re.compile(r"ул. [А-Яа-я]*, д. \d*, кв. \d, [А-Яа-я]*, [А-Яа-я]*")
        if not address_regex.match(value):
            raise ValueError("Адрес должен быть в формате 'ул. Ленина, д. 1, кв. 1, г. Москва, Россия'")
        return value
    @field_validator('timestamp')
    def validate_timestamp(cls, value):
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Временная метка должна быть в формате ISO 8601")
        return value

    @field_validator('gender')
    def validate_gender(cls, value):
        if value not in ['мужчина', 'женщина']:
            raise ValueError("Пол должен быть 'мужчина' или 'женщина'")
        return value

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        phone_regex = re.compile(r"^\+7\d{10}$")
        if not phone_regex.match(value):
            raise ValueError("Номер телефона должен быть в формате +7XXXXXXXXXX")
        return value

    @field_validator('date_of_birth')
    def validate_date_of_birth(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Дата рождения должна быть в формате 'YYYY-MM-DD'")
        return value
