from fastapi import FastAPI

from core.message_broker.kafka import startup_event, shutdown_event
from endpoints.applications import applications

app = FastAPI()

app.include_router(applications)


@app.on_event("startup")
async def on_startup():
    await startup_event()


@app.on_event("shutdown")
async def on_shutdown():
    await shutdown_event()
