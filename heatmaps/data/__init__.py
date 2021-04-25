"""Module containing all API interaction, data collection and normalization methods."""
from heatmaps.data.covid import Covid

from sanic import Sanic


# add all clients here as they are made
ALL_CLIENTS = {Covid}


async def collect_all_data(app: Sanic) -> None:
    """
    Entrypoint function to be used in the task loop.
    """
    for Client in ALL_CLIENTS:
        await Client(app).collect_data()
