from fastapi import APIRouter
from models.application import ApplicationsModel
from services.application import application_service
from models.validation_result import ValidationResultChecker

applications = APIRouter()


@applications.post("/", response_model=ValidationResultChecker)
async def create_application(application: ApplicationsModel) -> ValidationResultChecker:
    response_text = await application_service(application)
    return response_text
