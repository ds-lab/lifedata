import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from lifedata.annotations.sample import Sample
from lifedata.webapi.providers import provide_load_sample_display_data
from lifedata.webapi.samples import provide_db_sample_state
from lifedata.webapi.samples import provide_sample
from lifedata.webapi.samples import router

sample = Sample(id="1234")  # type: ignore


def load_sample_display_data(sample_id: str) -> str:
    return f"data-of-id-{sample_id}"


@fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[provide_sample] = lambda: sample
    app.dependency_overrides[provide_db_sample_state] = lambda: None
    app.dependency_overrides[
        provide_load_sample_display_data
    ] = lambda: load_sample_display_data
    return TestClient(app)


def test_retrieve_next_sample(client: TestClient) -> None:
    response = client.get("/samples/next/")

    assert response.status_code == 200

    assert response.json() == {
        "id": "1234",
        "data": "data-of-id-1234",
    }


def test_retrieve_sample_by_id(client: TestClient) -> None:
    response = client.get("/samples/by-id/abcd/")

    assert response.status_code == 200

    assert response.json() == {
        "id": "abcd",
        "data": "data-of-id-abcd",
    }


if __name__ == "__main__":
    pytest.main([__file__])
