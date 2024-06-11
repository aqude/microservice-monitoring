import asyncio
import json
from clickhouse_driver import Client
from aiokafka import AIOKafkaConsumer

from logger import Logger
from scheme.application import Application

VALIDATION_TOPIC = 'db_service'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

client = Client(host='localhost', port=9000)
logger = Logger()

async def handle_message(message) -> Application:
    try:
        data = json.loads(message.value.decode('utf-8'))
        application = Application(**data)
        return application
    except Exception as e:
        logger.new_event('main', 'handle_message', str(e), True)


async def load_data_from_db(application: Application):
    dataset = ", ".join([f"'{item}'" for item in application.to_dict().values()])
    client.execute(f"INSERT INTO application VALUES ({dataset})")
    logger.new_event('db_service', 'load_data', 'OK', False)


async def consume_and_load():
    consumer = AIOKafkaConsumer(
        VALIDATION_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="load_data_group",
        enable_auto_commit=True,
        auto_commit_interval_ms=5000,
    )
    await consumer.start()
    try:
        async for message in consumer:
            application: Application = await handle_message(message)

            await load_data_from_db(application)
    except Exception as e:
        logger.new_event('main', 'consume_and_load', str(e), True)

    finally:
        await consumer.stop()


asyncio.run(consume_and_load())
