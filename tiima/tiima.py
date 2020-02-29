import datetime
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import requests

from .settings import TIIMA_API_KEY, TIIMA_COMPANY_ID, TIIMA_PASSWORD, TIIMA_USERNAME


class TiimaSession(requests.Session):
    def __init__(self, company_id: str, api_key: str,) -> None:
        super().__init__()
        self.url_base = "https://www.tiima.com/rest/api/mobile/"
        self._set_default_headers()
        self._set_default_login(company_id=company_id, api_key=api_key)

    def _set_default_headers(self) -> None:
        self.headers.update(
            {
                "X-Tiima-Language": "en",
                "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.119 Mobile Safari/537.36",
            }
        )

    def _set_default_login(self, company_id: str, api_key: str) -> None:
        self.auth = (company_id, api_key)

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:  # type: ignore
        url = urljoin(self.url_base, url)

        return super().request(method, url, **kwargs)


class Tiima:
    """
    Usage:
        # Usage with env vars
        tiima = Tiima()
        tiima.login()

        # Setting auth variables explicitly
        tiima = Tiima(company_id="foo", api_key="bar)
        tiima.login(username="example@example.com", password="example")

        # Calling an API endpoint
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        print(tiima.workinghours(date=yesterday))
    """

    def __init__(
        self,
        company_id: str = TIIMA_COMPANY_ID,
        api_key: str = TIIMA_API_KEY,
    ) -> None:
        self.api = TiimaSession(company_id=company_id, api_key=api_key)

    def login(
        self,
        username: str = TIIMA_USERNAME,
        password: str = TIIMA_PASSWORD,
    ) -> None:
        login_data = {
            "username": username,
            "password": password,
            "clientVersion": "0.1",
            "deviceType": "Android",
            "deviceDescription": "OnePlus 7",
        }
        response = self.api.post("user/login", json=login_data)

        if response.status_code != 200:
            raise Exception(
                f"Login failed ({response.status_code}) with the credentials given for {TIIMA_USERNAME}. {response.text}"
            )
        json_response = response.json()
        token = json_response.get("token", None)

        if not token:
            raise Exception("No token returned during login")

        self.api.headers.update({"X-Tiima-Token": token})

    def __call_get(
        self, url: str, query_params: Optional[Dict[str, Any]] = None
    ) -> Any:
        if not query_params:
            query_params = {}

        response = self.api.get(url, params=query_params)
        if response.status_code != 200:
            raise Exception(
                f"Request to {url} failed with status code {response.status_code}. {response.text}"
            )
        return response.json()

    def __call_post(self, url: str, data: Optional[Dict[str, Any]] = None) -> Any:
        if not data:
            data = {}

        response = self.api.post(url, json=data)
        if response.status_code != 200:
            raise Exception(
                f"Request to {url} failed with status code {response.status_code}. {response.text}"
            )
        return response.json()

    def __parse_date(self, date: Union[datetime.datetime, str]) -> str:
        valid_date_structure = "%Y-%m-%d"
        if isinstance(date, str):
            try:
                datetime.datetime.strptime(date, valid_date_structure)
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            return date
        elif isinstance(date, datetime.datetime):
            return date.strftime(valid_date_structure)

    def reason_codes(self) -> Any:
        url = "reasoncodes"

        return self.__call_get(url)

    def user(self) -> Any:
        url = "user"

        return self.__call_get(url)

    def user_state(self) -> Any:
        url = "user/state"

        return self.__call_get(url)

    def user_enter(self, reason_code: int = 1) -> Any:
        url = "user/enter"
        data = {"reasonCode": reason_code}

        return self.__call_post(url, data=data)

    def user_leave(self, reason_code: int = 1) -> Any:
        url = "user/leave"
        data = {"reasonCode": reason_code}

        return self.__call_post(url, data=data)

    def user_to_lunch(self, reason_code: int = 1) -> Any:
        url = "user/toLunch"
        data = {"reasonCode": reason_code}

        return self.__call_post(url, data=data)

    def user_from_lunch(self, reason_code: int = 1) -> Any:
        url = "user/fromLunch"
        data = {"reasonCode": reason_code}

        return self.__call_post(url, data=data)

    def workinghours(self, date: Optional[Union[datetime.datetime, str]] = None) -> Any:
        if not date:
            date = datetime.datetime.now()

        url = "workinghours"
        query_params = {"date": self.__parse_date(date)}

        return self.__call_get(url, query_params=query_params)

    def calendar_plans(
        self,
        start_date: Union[datetime.datetime, str],
        end_date: Union[datetime.datetime, str],
    ) -> Any:
        url = "calendar/plans"
        query_params = {
            "startDate": self.__parse_date(start_date),
            "endDate": self.__parse_date(end_date),
        }

        return self.__call_get(url, query_params=query_params)

    def calendar_shifts(
        self,
        start_date: Union[datetime.datetime, str],
        end_date: Union[datetime.datetime, str],
    ) -> Any:
        url = "calendar/shifts"
        query_params = {
            "startDate": self.__parse_date(start_date),
            "endDate": self.__parse_date(end_date),
        }

        return self.__call_get(url, query_params=query_params)

    def bulletins(self) -> Any:
        url = "bulletins"

        return self.__call_get(url)

    def bulletins_mark(self, bulletin_id: str) -> Any:
        url = "bulletins/mark"
        data = {"bulletinId": bulletin_id}

        return self.__call_post(url, data=data)
