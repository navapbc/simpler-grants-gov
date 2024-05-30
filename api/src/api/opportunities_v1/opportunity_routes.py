import logging

import src.adapters.db as db
import src.adapters.db.flask_db as flask_db
import src.adapters.search as search
import src.adapters.search.flask_opensearch as flask_opensearch
import src.api.opportunities_v1.opportunity_schemas as opportunity_schemas
import src.api.response as response
from src.api.opportunities_v1.opportunity_blueprint import opportunity_blueprint
from src.auth.api_key_auth import api_key_auth
from src.logging.flask_logger import add_extra_data_to_current_request_logs
from src.services.opportunities_v1.get_opportunity import get_opportunity
from src.services.opportunities_v1.search_opportunities import search_opportunities
from src.util.dict_util import flatten_dict

logger = logging.getLogger(__name__)

# Descriptions in OpenAPI support markdown https://swagger.io/specification/
SHARED_ALPHA_DESCRIPTION = """
__ALPHA VERSION__

This endpoint in its current form is primarily for testing and feedback.

Features in this endpoint are still under heavy development, and subject to change. Not for production use.

See [Release Phases](https://github.com/github/roadmap?tab=readme-ov-file#release-phases) for further details.
"""

examples = {
    "example1": {
        "summary": "No filters",
        "value": {
            "pagination": {
                "order_by": "opportunity_id",
                "page_offset": 1,
                "page_size": 25,
                "sort_direction": "ascending",
            },
        },
    },
    "example2": {
        "summary": "All filters",
        "value": {
            "query": "research",
            "filters": {
                "agency": {"one_of": ["USAID", "ARPAH"]},
                "applicant_type": {
                    "one_of": ["state_governments", "county_governments", "individuals"]
                },
                "funding_category": {"one_of": ["recovery_act", "arts", "natural_resources"]},
                "funding_instrument": {"one_of": ["cooperative_agreement", "grant"]},
                "opportunity_status": {"one_of": ["forecasted", "posted"]},
            },
            "pagination": {
                "order_by": "opportunity_id",
                "page_offset": 1,
                "page_size": 25,
                "sort_direction": "descending",
            },
        },
    },
    "example3": {
        "summary": "Query & opportunity_status filters",
        "value": {
            "query": "research",
            "filters": {
                "opportunity_status": {"one_of": ["forecasted", "posted"]},
            },
            "pagination": {
                "order_by": "opportunity_id",
                "page_offset": 1,
                "page_size": 25,
                "sort_direction": "descending",
            },
        },
    },
}


@opportunity_blueprint.post("/opportunities/search")
@opportunity_blueprint.input(
    opportunity_schemas.OpportunitySearchRequestV1Schema,
    arg_name="search_params",
    examples=examples,
)
# many=True allows us to return a list of opportunity objects
@opportunity_blueprint.output(opportunity_schemas.OpportunitySearchResponseV1Schema())
@opportunity_blueprint.auth_required(api_key_auth)
@opportunity_blueprint.doc(description=SHARED_ALPHA_DESCRIPTION)
@flask_opensearch.with_search_client()
def opportunity_search(
    search_client: search.SearchClient, search_params: dict
) -> response.ApiResponse:
    add_extra_data_to_current_request_logs(flatten_dict(search_params, prefix="request.body"))
    logger.info("POST /v1/opportunities/search")

    opportunities, aggregations, pagination_info = search_opportunities(
        search_client, search_params
    )

    add_extra_data_to_current_request_logs(
        {
            "response.pagination.total_pages": pagination_info.total_pages,
            "response.pagination.total_records": pagination_info.total_records,
        }
    )
    logger.info("Successfully fetched opportunities")

    return response.ApiResponse(
        message="Success",
        data={
            "opportunities": opportunities,
            "facet_counts": aggregations,
            "pagination_info": pagination_info,
        },
        pagination_info=pagination_info,
    )


@opportunity_blueprint.get("/opportunities/<int:opportunity_id>")
@opportunity_blueprint.output(opportunity_schemas.OpportunityV1Schema())
@opportunity_blueprint.auth_required(api_key_auth)
@opportunity_blueprint.doc(description=SHARED_ALPHA_DESCRIPTION)
@flask_db.with_db_session()
def opportunity_get(db_session: db.Session, opportunity_id: int) -> response.ApiResponse:
    add_extra_data_to_current_request_logs({"opportunity.opportunity_id": opportunity_id})
    logger.info("GET /v1/opportunities/:opportunity_id")
    with db_session.begin():
        opportunity = get_opportunity(db_session, opportunity_id)

    return response.ApiResponse(message="Success", data=opportunity)
