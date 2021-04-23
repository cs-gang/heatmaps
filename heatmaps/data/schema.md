# Database document schema

All documents that go in the `api_responses` collection must be of the following schema:
```json
{
    "api": string,
    "data": [
        {
            "country": string,
            "value": int
        }
    ]
}
```
