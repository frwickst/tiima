# Tiima

A Python wrapper around the Visma Tiima mobile REST API

## Installation

### PIP
`pip install tiima`

### Poetry
`poetry add tiima`


## Usage


```
from tiima import Tiima

# Usage with env vars
tiima = Tiima()
tiima.login()

# Setting auth variables explicitly
tiima = Tiima(company_id="foo", api_key="bar)
tiima.login(username="example@example.com", password="example")

# Calling an API endpoint
print(tiima.user())
```

### Configuration

Authentication can be done either explcitly or by settings the following environment variables:


| Variable          | Description                          |
| ----------------- | ------------------------------------ |
| TIIMA_USERNAME    | Users Tiima username (email)         |
| TIIMA_PASSWORD    | Users Tiima password                 |
| TIIMA_COMPANY_ID  | Users company id (usually all caps)  |
| TIIMA_API_KEY     | Tiima API Key                        |


## Disclaimer

This software has no connection to Visma, nor is it in any way endorsed by Visma or any other company
affiliated with the product (Visma Tiima). This project was created to make it easier for developers
to use the API and for them to be able to create their own application around the API.

## License

MIT
