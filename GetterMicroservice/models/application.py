from pydantic import BaseModel


class ApplicationsModel(BaseModel):
    timestamp: str = None
    full_name: str = None
    user_id: str = None
    email: str = None
    phone_number: str = None
    address: str = None
    date_of_birth: str = None
    gender: str = None
    event_type: str = None
    event_description: str = None
    text: str = None
