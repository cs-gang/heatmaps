from abc import ABC, abstractmethod
from numbers import Number
from typing import Any, Mapping, Optional

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
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

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.app.ctx.db["api_responses"]

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
    def normalize(self, value: Number, total: Number) -> float:
        """
        Normalize the value of some data set to a 10-point scale.
        Normalized values need not be stored; but be calculated when needed.
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
        Entrypoint function; only this function is expected to be used externally (probably in a background task).
        """
        pass

    @abstractmethod
    async def retrieve_data(self, projection: Optional[Mapping[Any, Any]] = None) -> BaseModel:
        """
        Function to retrieve stored data from the database.
        This function should retrieve the latest document for the corresponding API
        by default.

        Arguments:
            projection: A projection to be used in the db query.
                A projection essentially limits the data retrieved from a document.
                This argument can be used in case a single API client is storing multiple
                plottable data points.

        Returns:
            The validated BaseModel for the corresponding API.

        NOTE: as `api_responses` is a capped collection
              (refer: https://docs.mongodb.com/manual/core/capped-collections/)
              we do not need to check the insertion datetime to retrieve the
              latest document which is usually the document we always need
        """
        pass
