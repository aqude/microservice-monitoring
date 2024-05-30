from dataclasses import dataclass

@dataclass
class Application:
    timestamp: str
    full_name: str 
    user_id: str
    email: str
    phone_number: str
    address: str 
    date_of_birth: str 
    gender: str 
    event_description: str 