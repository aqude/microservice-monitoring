from fastapi import APIRouter, HTTPException
from models.application import ApplicationsModel
from services.application import application_service
from models.validation_result import ValidationResultChecker

applications = APIRouter()


# @applications.post("/", response_model=ValidationResultChecker)
# async def create_application(application: ApplicationsModel) -> ValidationResultChecker:
#     response_text = await application_service(application)
#     if not response_text.success:
#         raise HTTPException(status_code=400, detail=response_text.msg)
#     return response_text

@applications.post("/")
async def create_application(application: ApplicationsModel) -> dict:
    await application_service(application)
    return {"success": True}