"""Server listeners and logging."""
import os
from asyncio import AbstractEventLoop

from aiohttp import ClientSession
from dotenv import find_dotenv, load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid
from sanic import Sanic

from heatmaps import data
from heatmaps.utils import Loop

load_dotenv(find_dotenv())


app = Sanic("heatmaps")

# initializing jinja2 templates
app.ctx.env = Environment(
    loader=PackageLoader("heatmaps", "templates"),
    autoescape=select_autoescape(["html"]),
    enable_async=True,
)


async def collect_data() -> None:
    """Background task to collect data from APIs and insert it into the database."""
    await data.collect_all_data(app)


# server event listeners
@app.listener("before_server_start")
async def before_server_start(app: Sanic, loop: AbstractEventLoop) -> None:
    app.ctx.http_session = ClientSession(loop=loop)
    logger.trace("HTTP ClientSession made")


@app.listener("after_server_start")
async def start_data_collection(app: Sanic, loop: AbstractEventLoop) -> None:
    # create capped collection to store the data in case it isn't made already
    app.ctx.db = AsyncIOMotorClient(os.environ.get("DATABASE_URL"), io_loop=loop)[
        "heatmaps-db"
    ]
    try:
        await app.ctx.db.create_collection("api_responses", capped=True, size=1000000)
    except CollectionInvalid:
        pass
    # start the registered task loops
    Loop(collect_data, loop=loop, minutes=1).start()  # TODO: increase this
    logger.info("Background task started")


@app.listener("before_server_stop")
async def close_http_session(app: Sanic, loop: AbstractEventLoop) -> None:
    await app.ctx.http_session.close()
    logger.info("Heatmaps shut down")
