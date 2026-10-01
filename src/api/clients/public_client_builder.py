from httpx import Client

from config import settings


def public_client_builder() -> Client:
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
    )
