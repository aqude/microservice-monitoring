import asyncio
import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from pydantic import ValidationError

from applications import Application
from models.validation_result import ValidationResultChecker

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
VALIDATION_TOPIC = 'validation'
RESULT_TOPIC = 'validation_result'
NEXT_TOPIC = 'db_service'


async def handle_message(message):
    try:
        data = json.loads(message.value.decode('utf-8'))
        user_id = data.get('user_id')
        application = Application(**data)

        validation_result = ValidationResultChecker(success=True, msg='OK', user_id=user_id)

        return validation_result.dict(), user_id, data
    except ValidationError as e:
        errors = e.errors()
        error_message = "; ".join([f"{err['loc'][0]}: {err['msg']}\n" for err in errors])
        validation_result = ValidationResultChecker(success=False, msg=error_message,
                                                    user_id=data.get('user_id', 'unknown'))
        return validation_result.dict(), None, None


async def consume_and_validate():
    consumer = AIOKafkaConsumer(
        VALIDATION_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="validation_group"
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    await producer.start()
    await consumer.start()

    try:
        async for message in consumer:
            validation_result, user_id, data = await handle_message(message)
            await producer.send_and_wait(RESULT_TOPIC, json.dumps(validation_result).encode('utf-8'))

            if validation_result['success'] and data:
                await producer.send_and_wait(NEXT_TOPIC, json.dumps(data).encode('utf-8'))
    except Exception as e:
        validation_result = ValidationResultChecker(success=False, msg=str(e), user_id=None)
        await producer.send_and_wait(RESULT_TOPIC, json.dumps(validation_result.dict()).encode('utf-8'))
    finally:
        await consumer.stop()
        await producer.stop()


asyncio.run(consume_and_validate())
