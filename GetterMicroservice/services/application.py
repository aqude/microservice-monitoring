from models.application import ApplicationsModel
from core.message_broker.kafka import send_to_kafka, get_validation_result
# from models.validation_result import ValidationResult, ValidationResultChecker


async def application_service(application: ApplicationsModel):
    apl = ApplicationsModel(
        timestamp=application.timestamp,
        full_name=application.full_name,
        user_id=application.user_id,
        email=application.email,
        phone_number=application.phone_number.replace(" ", "").replace("(", "").replace(")", "").replace("-", ""),
        address=application.address,
        date_of_birth=application.date_of_birth,
        gender=application.gender,
        event_type=application.event_type,
        event_description=application.event_description,
        text=application.text
    )
    await send_to_kafka(apl)
    # result = await get_validation_result(application.user_id)
    # return result
