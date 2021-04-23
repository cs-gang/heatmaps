"""Server listeners and logging."""
import os
from asyncio import BaseEventLoop

from aiohttp import ClientSession
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic
from sanic.request import Request
from sanic.response import json, HTTPResponse

load_dotenv(find_dotenv())


app = Sanic("heatmaps")


@app.listener("before_server_start")
async def before_server_start(app: Sanic, loop: BaseEventLoop) -> None:
    app.ctx.db = AsyncIOMotorClient(os.environ.get("DATABASE_URL"))["heatmaps-db"]
    logger.info("Database client made")
    app.ctx.http_session = ClientSession(loop=loop)
    logger.info("HTTP ClientSession made")
    # TODO: start data collection routine here. look into: sanic background tasks.


@app.listener("after_server_start")
async def after_server_start(app: Sanic, loop: BaseEventLoop) -> None:
    logger.info("Heatmaps running!")


@app.listener("before_server_stop")
async def close_db(app: Sanic, loop: BaseEventLoop) -> None:
    await app.ctx.http_session.close()
    logger.info("Heatmaps shut down")


@app.route("/")
async def index(request: Request) -> HTTPResponse:
    # TODO: change this
    return json({"hello": "world"})
