from abc import ABC, abstractmethod
from numbers import Number
from typing import Any

from sanic import Sanic


class AbstractAPIClient(ABC):
    """
    Abstract base class representing an API client.
    Every API that we use must have a corresponding API client class made,
    which inherits from this class, and overrides it's abstract methods.

    Any constants must be set as class variables.
    """

    def __init__(self, app: Sanic) -> None:
        self.app = app

    @abstractmethod
    async def fetch_data(self) -> Any:
        """
        Method to make a request to the API, and return the API response.
        Although the return type has been annotated as `Any`, it will
        most likely be `dict`.
        """
        pass

    @abstractmethod
    def parse_data(self, data: Any) -> Any:
        """
        Parse the raw response returned by the `AbstractAPIClient.fetch_data`
        coroutine.
        """
        pass

    @abstractmethod
    def normalize(self, value: Number) -> float:
        """
        Normalize the value of some data set to a 10-point scale.
        To be used iteratively, for data for all countries in the `AbstractAPIClient.parse_data`
        method.
        """
        pass

    @abstractmethod
    async def insert_data(self, data: dict) -> None:
        """
        Insert the processed data into the corresponding collection in the database.
        """
        pass

    @abstractmethod
    async def collect_data(self) -> None:
        """
        Entrypoint function; only this function is expected to be used externally.
        """
        pass
