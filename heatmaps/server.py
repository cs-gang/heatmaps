"""Server listeners and logging."""
import os
from asyncio import BaseEventLoop

from aiohttp import ClientSession
from dotenv import find_dotenv, load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic
from sanic.request import Request
from sanic.response import html, HTTPResponse

from heatmaps.utils import render_page

load_dotenv(find_dotenv())


app = Sanic("heatmaps")

# initialize database client
app.ctx.db = AsyncIOMotorClient(os.environ.get("DATABASE_URL"))["heatmaps-db"]

# initializing jinja2 templates
app.ctx.env = Environment(
    loader=PackageLoader("heatmaps", "templates"),
    autoescape=select_autoescape(["html"]),
    enable_async=True,
)


@app.listener("before_server_start")
async def before_server_start(app: Sanic, loop: BaseEventLoop) -> None:
    # create capped collection to store the data in case it isn't made already
    await app.ctx.db.create_collection("api_responses", capped=True, size=1000)
    app.ctx.http_session = ClientSession(loop=loop)
    logger.info("HTTP ClientSession made")
    # TODO: start data collection routine here. look into: sanic background tasks.


@app.listener("before_server_stop")
async def close_db(app: Sanic, loop: BaseEventLoop) -> None:
    await app.ctx.http_session.close()
    logger.info("Heatmaps shut down")


@app.route("/")
async def index(request: Request) -> HTTPResponse:
    output = await render_page(app.ctx.env, file="index.html")
    return html(output)
