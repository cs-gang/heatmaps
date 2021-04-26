"""Module containing all API interaction, data collection and normalization methods."""
from abc import ABCMeta
from typing import Mapping, Optional, Type

from sanic import Sanic
from pydantic import BaseModel

from heatmaps.data.abc import AbstractAPIClient
from heatmaps.data.covid import Covid


# add all API clients here
ALL_CLIENTS: Mapping[str, Type[AbstractAPIClient]] = {"covid": Covid}


async def collect_all_data(app: Sanic) -> None:
    """
    Entrypoint function to be used in the task loop.
    """
    for Client in ALL_CLIENTS.values():
        await Client(app).collect_data()


async def retrieve_client_data(app: Sanic, client_name: str) -> Optional[BaseModel]:
    """
    Entrypoint function to retrieve stored heatmap data.

    Arguments:
        client: The name of the Client whose data needs to be retrieved.
    """
    client: AbstractAPIClient = ALL_CLIENTS[client_name.lower()](app)

    return await client.retrieve_data()
