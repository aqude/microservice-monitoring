import asyncio
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import FastAPI
from models.application import ApplicationsModel
from models.validation_result import ValidationResultChecker

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
VALIDATION_TOPIC = 'validation'
RESULT_TOPIC = 'validation_result'
producer: AIOKafkaProducer = None
app = FastAPI()


async def startup_event():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()


async def shutdown_event():
    await producer.stop()


async def send_to_kafka(application):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        await producer.send_and_wait(VALIDATION_TOPIC, json.dumps(application.dict()).encode('utf-8'))
    finally:
        await producer.stop()

async def get_validation_result(user_id: str) -> ValidationResultChecker:
    consumer = AIOKafkaConsumer(
        RESULT_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="validation_group",
        enable_auto_commit=True,
        auto_commit_interval_ms=5000,
    )
    await consumer.start()
    try:
        timeout = 10  # Тайм-аут ожидания результата в секундах
        end_time = asyncio.get_event_loop().time() + timeout
        async for msg in consumer:
            result = ValidationResultChecker(**json.loads(msg.value.decode('utf-8')))
            if result.user_id == user_id:
                return result
            if asyncio.get_event_loop().time() > end_time:
                break
        return ValidationResultChecker(success=False, msg="User not found or timeout exceeded")
    except Exception as e:
        print(f"Error while consuming messages: {e}")
        return ValidationResultChecker(success=False, msg=str(e))
    finally:
        await consumer.stop()
