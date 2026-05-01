from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_app_is_fastapi_instance(client: TestClient) -> None:
    assert isinstance(client.app, FastAPI)
