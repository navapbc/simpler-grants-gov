import uuid

import opensearchpy
import pytest

from src.adapters.opensearch.opensearch_client import get_opensearch_client

########################################
# This is a placeholder set of tests,
# we'll evolve / change the structure
# as we continue developing this
#
# Just wanted something simple so I can verify
# the early steps of this setup are working
# before we actually have code to use
########################################


@pytest.fixture(scope="session")
def search_client() -> opensearchpy.OpenSearch:
    # TODO - move this to conftest
    return get_opensearch_client()


@pytest.fixture(scope="session")
def opportunity_index(search_client):
    # TODO - will adjust this in the future to use utils we'll build
    # for setting up / aliasing indexes. For now, keep it simple

    index_name = f"test_{uuid.uuid4().int}_opportunity"

    search_client.indices.create(index_name, body={})

    try:
        yield index_name
    finally:
        search_client.indices.delete(index_name)


def test_index_is_running(search_client, opportunity_index):
    existing_indexes = search_client.cat.indices(format="json")

    found_opportunity_index = False
    for index in existing_indexes:
        if index["index"] == opportunity_index:
            found_opportunity_index = True
            break

    assert found_opportunity_index is True

    # Add a few records to the index

    record1 = {
        "opportunity_id": 1,
        "opportunity_title": "Research into how to make a search engine",
        "opportunity_status": "posted",
    }
    record2 = {
        "opportunity_id": 2,
        "opportunity_title": "Research about words, and more words!",
        "opportunity_status": "forecasted",
    }

    search_client.index(index=opportunity_index, body=record1, id=1, refresh=True)
    search_client.index(index=opportunity_index, body=record2, id=2, refresh=True)

    search_request = {
        "query": {
            "bool": {
                "must": {
                    "simple_query_string": {"query": "research", "fields": ["opportunity_title"]}
                }
            }
        }
    }
    response = search_client.search(index=opportunity_index, body=search_request)
    assert response["hits"]["total"]["value"] == 2

    filter_request = {
        "query": {"bool": {"filter": [{"terms": {"opportunity_status": ["forecasted"]}}]}}
    }
    response = search_client.search(index=opportunity_index, body=filter_request)
    assert response["hits"]["total"]["value"] == 1
