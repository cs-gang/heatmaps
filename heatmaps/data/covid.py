""""Covid data collection from the `disease.sh` API."""
from typing import Optional

from loguru import logger

from heatmaps.data import abc


class Covid(abc.AbstractAPIClient):
    API_URL = "https://disease.sh/"

    async def fetch_data(self) -> Optional[dict]:
        async with self.app.ctx.http_session.get(
            Covid.API_URL + "/v3/covid-19/countries"
        ) as resp:
            if resp.status == 200:
                logger.info("<COVID> Fetched COVID data")
                return await resp.json()
            else:
                logger.warning(
                    "<COVID> API returned non-200 status code, could not fetch data"
                )
