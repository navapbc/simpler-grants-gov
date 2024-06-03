import logging

import src.adapters.db as db
import src.adapters.db.flask_db as flask_db
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


@opportunity_blueprint.post("/opportunities/search")
@opportunity_blueprint.input(
    opportunity_schemas.OpportunitySearchRequestV1Schema, arg_name="search_params"
)
# many=True allows us to return a list of opportunity objects
@opportunity_blueprint.output(opportunity_schemas.OpportunityV1Schema(many=True))
@opportunity_blueprint.auth_required(api_key_auth)
@opportunity_blueprint.doc(description=SHARED_ALPHA_DESCRIPTION)
def opportunity_search(search_params: dict) -> response.ApiResponse:
    add_extra_data_to_current_request_logs(flatten_dict(search_params, prefix="request.body"))
    logger.info("POST /v1/opportunities/search")

    opportunities, pagination_info = search_opportunities(search_params)

    add_extra_data_to_current_request_logs(
        {
            "response.pagination.total_pages": pagination_info.total_pages,
            "response.pagination.total_records": pagination_info.total_records,
        }
    )
    logger.info("Successfully fetched opportunities")

    return response.ApiResponse(
        message="Success", data=opportunities, pagination_info=pagination_info
    )


@opportunity_blueprint.get("/opportunities/<int:opportunity_id>")
@opportunity_blueprint.output(opportunity_schemas.OpportunityGetResponseV1Schema)
@opportunity_blueprint.auth_required(api_key_auth)
@opportunity_blueprint.doc(description=SHARED_ALPHA_DESCRIPTION)
@flask_db.with_db_session()
def opportunity_get(db_session: db.Session, opportunity_id: int) -> response.ApiResponse:
    add_extra_data_to_current_request_logs({"opportunity.opportunity_id": opportunity_id})
    logger.info("GET /v1/opportunities/:opportunity_id")
    with db_session.begin():
        opportunity = get_opportunity(db_session, opportunity_id)

    print(opportunity)

    return response.ApiResponse(message="Success", data=opportunity)

from flask import Response, stream_with_context, send_file, redirect
import boto3

@opportunity_blueprint.get("/opportunities/<int:opportunity_id>/attachment/<int:attachment_id>")
@opportunity_blueprint.output({}, status_code=302)
# no auth for the moment
def get_opportunity_file(opportunity_id: int, attachment_id: int):
    # TODO - In a real implementation, we'd use these IDs to:
    # * Query the DB to get the path of the file (presumably S3 - I don't think we want these files in the DB)
    # * Fetch/stream the file from S3


    s3 = boto3.client("s3", endpoint_url="http://localstack:4566")

    # First time need to run this
    #s3.create_bucket(Bucket="myfunbucket")
    #with open("myfile.txt", "rb") as myfile:
    #    s3.upload_fileobj(myfile, "myfunbucket", "myfile.txt")


    url = s3.generate_presigned_url("get_object", Params={"Bucket": "myfunbucket", "Key": "myfile.txt"})

    print(url)
    # TODO - because we're hitting localstack inside the docker container, the URL generated is for inside
    # to make that work, we need to fix the path - I'm sure there is a better way to do this (changing the endpoint URL to the outside one?)
    x = url.replace("localstack", "localhost")
    print(x)

    return redirect(x, 302)