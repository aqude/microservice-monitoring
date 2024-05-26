from pydantic import BaseModel

class ValidationResult(BaseModel):
    success: bool
    msg: str

class ValidationResultChecker(ValidationResult):
    user_id: str