"""Index page route handling."""
from sanic.request import Request
from sanic.response import html, json, HTTPResponse

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

    # TODO: create function to retrieve heatmap data from db

    # output = await render_page(app.ctx.env, file="index.html", heatmap=topic)
    # return html(output)

    return json(
        {
            "topic": topic,
            "heatmap_data": {
                "hi": "i didn't finish making this yet",
                "but": "it will come in the next commit",
            },
        }
    )
