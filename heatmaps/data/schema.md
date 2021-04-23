# Database document schema

All documents that go in the `api_responses` collection must be of the following schema:

## COVID-19 data
```json
{
    "api": "covid",
    "data": [
        {
            "country": string,
            "statistics": [
                {
                    "stat": string,
                    "raw_count": int,
                    "normalized": float
                }
            ]
        }
    ]
}
```
