"""Index page route handling."""
from sanic.request import Request
from sanic.response import html, HTTPResponse

from heatmaps.data import retrieve_client_data
from heatmaps.server import app

from heatmaps.utils import render_page


@app.get("/")
async def index(request: Request) -> HTTPResponse:
    # user's heatmap choice is sent over as query args
    # refer https://sanic.readthedocs.io/en/18.12.0/sanic/request_data.html
    query_args = request.args
    topic = query_args.get(
        "heatmap"
    )  # if the key doesn't exist, it means the user just got to the page

    if not topic:  # TODO: change this
        output = await render_page(app.ctx.env, file="index.html")
        return html(output)

    heatmap_data = (await retrieve_client_data(app, topic)).dict()
    heatmap_data.pop("time")

    output = await render_page(app.ctx.env, file="index.html", heatmap=topic)
    return html(output)
