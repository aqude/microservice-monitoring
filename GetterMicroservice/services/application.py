from models.application import ApplicationsModel
from core.message_broker.kafka import send_to_kafka, get_validation_result
from models.validation_result import ValidationResult, ValidationResultChecker


async def application_service(application: ApplicationsModel) -> ValidationResultChecker:
    await send_to_kafka(application)
    result = await get_validation_result(application.user_id)
    return result
