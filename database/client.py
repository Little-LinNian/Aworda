from motor import motor_asyncio
import asyncio
import loguru

client: motor_asyncio.AsyncIOMotorClient = None
loop = asyncio.get_event_loop()
loguru.logger.info("Connecting to database")


def init_db(loop: asyncio.AbstractEventLoop):
    global client
    client = motor_asyncio.AsyncIOMotorClient(io_loop=loop)


loguru.logger.info("Connected to database")


def get_client():
    if not client:
        raise Exception("Database not initialized")
    return client
