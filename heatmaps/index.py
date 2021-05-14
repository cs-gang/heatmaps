"""Index page route handling."""
import json as js

from sanic.request import Request
from sanic.response import html, json, HTTPResponse

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
        return json(
            {
                "hi bro": "you didn't specify an API bro",
                "try:": "domain.com/?heatmap=covid",
            }
        )

    heatmap_data = (await retrieve_client_data(app, topic)).dict()
    heatmap_data.pop("time")

    # output = await render_page(app.ctx.env, file="index.html", heatmap=topic)
    # return html(output)

    # THIS IS TEST CODE
    response_string = f"<html><body>{js.dumps(heatmap_data, indent=4)}</body></html>"
    return html(response_string)
