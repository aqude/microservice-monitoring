import asyncio
import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from pydantic import ValidationError

from applications import Application
from logger import Logger
from models.validation_result import ValidationResultChecker

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
VALIDATION_TOPIC = 'validation'
NEXT_TOPIC = 'db_service'

logger = Logger()

async def handle_message(message):
    try:
        data = json.loads(message.value.decode('utf-8'))
        user_id = data.get('user_id')
        application = Application(**data)

        validation_result = ValidationResultChecker(success=True, msg='OK', user_id=user_id)

        return validation_result.dict(), user_id, data
    except ValidationError as e:
        errors = e.errors()
        error_message = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in errors])
        validation_result = ValidationResultChecker(success=False, msg=error_message,
                                                    user_id=data.get('user_id', 'unknown'))
        logger.new_event('validation_service', 'validation', error_message, True)
        return validation_result.dict(), None, None
    except json.JSONDecodeError as e:
        error_message = f"JSONDecodeError: {str(e)}"
        validation_result = ValidationResultChecker(success=False, msg=error_message, user_id='unknown')
        logger.new_event('validation_service', 'validation', error_message, True)
        return validation_result.dict(), None, None
    except Exception as e:
        error_message = f"UnexpectedError: {str(e)}"
        validation_result = ValidationResultChecker(success=False, msg=error_message, user_id='unknown')
        logger.new_event('validation_service', 'validation', error_message, True)
        return validation_result.dict(), None, None


async def consume_and_validate():
    consumer = AIOKafkaConsumer(
        VALIDATION_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="validation_group",
        enable_auto_commit=True,
        auto_commit_interval_ms=5000,
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    await producer.start()
    await consumer.start()

    try:
        async for message in consumer:
            validation_result, user_id, data = await handle_message(message)
            logger.new_event('validation_service', 'validation', validation_result['msg'], not validation_result['success'])

            if validation_result['success'] and data:
                await producer.send_and_wait(NEXT_TOPIC, json.dumps(data).encode('utf-8'))
    except Exception as e:
        logger.new_event('validation_service', 'error', str(e), True)
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(consume_and_validate())
