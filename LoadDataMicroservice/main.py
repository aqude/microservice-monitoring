import asyncio
import json
from clickhouse_driver import Client
from aiokafka import AIOKafkaConsumer

from scheme.application import Application

VALIDATION_TOPIC = 'db_service'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

client = Client(host='localhost', port=8123)


async def handle_message(message) -> Application:
    try:
        data = json.loads(message.value.decode('utf-8'))
        application = Application(**data)
        return application
    except Exception as e:
        pass


async def load_data_from_db(application: Application):
    await client.execute('INSERT INTO application VALUES', application.dict())


async def consume_and_load():
    consumer = AIOKafkaConsumer(
        VALIDATION_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="load_data_group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            application: Application = await handle_message(message)

            await load_data_from_db(application)
    except Exception as e:
        print(e)

    finally:
        await consumer.stop()


asyncio.run(consume_and_load())
