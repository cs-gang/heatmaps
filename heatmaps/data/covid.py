""""Classes and models for handling COVID data from the `disease.sh` API."""
from datetime import datetime
from typing import List, Literal, Mapping, Optional, Union

from loguru import logger
from pydantic import BaseModel

from heatmaps.data import abc


class Statistic(BaseModel):
    """
    Represents a statistic dictionary. (Refer `schema.md`)
    """

    stat: str
    count: int


class Country(BaseModel):
    """
    Represents a country's data in the format that it is stored in the database.
    """

    country: str
    population: int
    statistics: List[Statistic]


class CovidDataDocument(BaseModel):
    api: str
    time: datetime
    data: List[Country]


class Covid(abc.AbstractAPIClient):
    API_URL = "https://disease.sh/"
    SAVED_STATS = {"cases", "todayCases", "deaths", "todayDeaths", "recovered", "tests"}

    async def fetch_data(self) -> Optional[list]:  # the endpoint returns a list
        async with self.app.ctx.http_session.get(
            Covid.API_URL + "v3/covid-19/countries"
        ) as resp:
            if resp.status == 200:
                logger.trace("<COVID> Fetched COVID data")
                return await resp.json()
            else:
                logger.warning(
                    f"<COVID> API returned non-200 status code ({resp.status}), could not fetch data"
                )

    def parse_data(self, data: list) -> dict:
        final = {"api": "covid", "time": datetime.utcnow(), "data": []}

        for country in data:
            country_dict = {
                "country": country["country"],
                "population": country["population"],
                "statistics": [],
            }

            for stat in Covid.SAVED_STATS:
                country_dict["statistics"].append(
                    {"stat": stat, "count": country[stat]}
                )

            final["data"].append(country_dict)

        # validation using pydantic (this eliminates the need to test this function)
        CovidDataDocument.parse_obj(final)

        logger.trace("<COVID> Data parsed")
        return final

    async def insert_data(self, data: dict) -> None:
        await self.collection.replace_one({"api": "covid"}, data, upsert=True)
        logger.info("<COVID> Data inserted to database")

    def normalize(self, value: int, total: int) -> float:
        # TODO: think this through, and write tests
        return (value / total) * 10

    async def collect_data(self) -> None:
        raw = await self.fetch_data()
        if raw is None:
            logger.error("<COVID> Data could not be retrieved, stopping collection")
            return
        parsed = self.parse_data(raw)
        await self.insert_data(parsed)
        logger.info("<COVID> Data collection completed")

    async def retrieve_data(self) -> Optional[CovidDataDocument]:
        """
        Entrypoint function to retrieve stored data on-demand.

        Returns:
            CovidDataDocument: A Pydantic validated model
        """
        data = await self.collection.find_one({"api": "covid"})

        if data is None:
            logger.warning("<COVID> No pre-existing data in the database")
            return

        return CovidDataDocument.parse_obj(data)


StatisticType = Union[
    Literal["cases"],
    Literal["todayCases"],
    Literal["deaths"],
    Literal["todayDeaths"],
    Literal["recovered"],
    Literal["tests"],
]


def filter_by_stat(data: CovidDataDocument, stat: StatisticType) -> List[Mapping]:
    """
    Filters the entire COVID data stored in the database
    to leave just the relevant statistic.
    """
    out = []

    for country in data.data:
        new_country = {"country": country.country, "population": country.population}

        for statistic_dict in country.statistics:
            if statistic_dict.stat == stat:
                new_country["statistics"] = statistic_dict
                break

        out.append(new_country)

    return out
