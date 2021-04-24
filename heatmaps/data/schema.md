# Database document schema

All documents that go in the `api_responses` collection must be of the following schema:

## COVID-19 data
```json
{
    "api": "covid",
    "time": datetime[utc],
    "data": [
        {
            "country": string,
            "population": int,
            "statistics": [
                {
                    "stat": string,
                    "count": int,
                }
            ]
        }
    ]
}
```
