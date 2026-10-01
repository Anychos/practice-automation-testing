from typing import Any

from httpx import URL, Client, QueryParams, Response


class BaseAPIClient:
    def __init__(self, client: Client):
        self.client = client

    def close(self):
        self.client.close()

    def get(
        self,
        *,
        url: str | URL,
        params: QueryParams | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        return self.client.get(url=url, params=params, headers=headers)

    def post(
        self,
        *,
        url: str | URL,
        params: QueryParams | None = None,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
        files: str | None = None,
    ) -> Response:
        return self.client.post(
            url=url, params=params, headers=headers, json=json, files=files
        )

    def put(
        self,
        *,
        url: str | URL,
        params: QueryParams | None = None,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
        files: str | None = None,
    ) -> Response:
        return self.client.put(
            url=url, params=params, headers=headers, json=json, files=files
        )

    def patch(
        self,
        *,
        url: str | URL,
        params: QueryParams | None = None,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
        files: str | None = None,
    ) -> Response:
        return self.client.patch(
            url=url, params=params, headers=headers, json=json, files=files
        )

    def delete(
        self,
        *,
        url: str | URL,
        params: QueryParams | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        return self.client.delete(url=url, params=params, headers=headers)
