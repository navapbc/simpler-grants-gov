from src.constants.lookup_constants import (
    ApplicantType,
    FundingCategory,
    FundingInstrument,
    OpportunityStatus,
)
from src.db.models.opportunity_models import (
    Opportunity,
    OpportunityAssistanceListing,
    OpportunitySummary,
)


def get_search_request(
    page_offset: int = 1,
    page_size: int = 5,
    order_by: str = "opportunity_id",
    sort_direction: str = "descending",
    query: str | None = None,
    funding_instrument_one_of: list[FundingInstrument] | None = None,
    funding_category_one_of: list[FundingCategory] | None = None,
    applicant_type_one_of: list[ApplicantType] | None = None,
    opportunity_status_one_of: list[OpportunityStatus] | None = None,
    agency_one_of: list[str] | None = None,
):
    req = {
        "pagination": {
            "page_offset": page_offset,
            "page_size": page_size,
            "order_by": order_by,
            "sort_direction": sort_direction,
        }
    }

    filters = {}

    if funding_instrument_one_of is not None:
        filters["funding_instrument"] = {"one_of": funding_instrument_one_of}

    if funding_category_one_of is not None:
        filters["funding_category"] = {"one_of": funding_category_one_of}

    if applicant_type_one_of is not None:
        filters["applicant_type"] = {"one_of": applicant_type_one_of}

    if opportunity_status_one_of is not None:
        filters["opportunity_status"] = {"one_of": opportunity_status_one_of}

    if agency_one_of is not None:
        filters["agency"] = {"one_of": agency_one_of}

    if len(filters) > 0:
        req["filters"] = filters

    if query is not None:
        req["query"] = query

    return req


#####################################
# Validation utils
#####################################


def validate_opportunity(db_opportunity: Opportunity, resp_opportunity: dict):
    assert db_opportunity.opportunity_id == resp_opportunity["opportunity_id"]
    assert db_opportunity.opportunity_number == resp_opportunity["opportunity_number"]
    assert db_opportunity.opportunity_title == resp_opportunity["opportunity_title"]
    assert db_opportunity.agency == resp_opportunity["agency"]
    assert db_opportunity.category == resp_opportunity["category"]
    assert db_opportunity.category_explanation == resp_opportunity["category_explanation"]

    validate_opportunity_summary(db_opportunity.summary, resp_opportunity["summary"])
    validate_assistance_listings(
        db_opportunity.opportunity_assistance_listings,
        resp_opportunity["opportunity_assistance_listings"],
    )

    assert db_opportunity.opportunity_status == resp_opportunity["opportunity_status"]


def validate_opportunity_summary(db_summary: OpportunitySummary, resp_summary: dict):
    if db_summary is None:
        assert resp_summary is None
        return

    assert db_summary.summary_description == resp_summary["summary_description"]
    assert db_summary.is_cost_sharing == resp_summary["is_cost_sharing"]
    assert db_summary.is_forecast == resp_summary["is_forecast"]
    assert str(db_summary.close_date) == str(resp_summary["close_date"])
    assert db_summary.close_date_description == resp_summary["close_date_description"]
    assert str(db_summary.post_date) == str(resp_summary["post_date"])
    assert str(db_summary.archive_date) == str(resp_summary["archive_date"])
    assert db_summary.expected_number_of_awards == resp_summary["expected_number_of_awards"]
    assert (
        db_summary.estimated_total_program_funding
        == resp_summary["estimated_total_program_funding"]
    )
    assert db_summary.award_floor == resp_summary["award_floor"]
    assert db_summary.award_ceiling == resp_summary["award_ceiling"]
    assert db_summary.additional_info_url == resp_summary["additional_info_url"]
    assert (
        db_summary.additional_info_url_description
        == resp_summary["additional_info_url_description"]
    )

    assert str(db_summary.forecasted_post_date) == str(resp_summary["forecasted_post_date"])
    assert str(db_summary.forecasted_close_date) == str(resp_summary["forecasted_close_date"])
    assert (
        db_summary.forecasted_close_date_description
        == resp_summary["forecasted_close_date_description"]
    )
    assert str(db_summary.forecasted_award_date) == str(resp_summary["forecasted_award_date"])
    assert str(db_summary.forecasted_project_start_date) == str(
        resp_summary["forecasted_project_start_date"]
    )
    assert db_summary.fiscal_year == resp_summary["fiscal_year"]

    assert db_summary.funding_category_description == resp_summary["funding_category_description"]
    assert (
        db_summary.applicant_eligibility_description
        == resp_summary["applicant_eligibility_description"]
    )

    assert db_summary.agency_code == resp_summary["agency_code"]
    assert db_summary.agency_name == resp_summary["agency_name"]
    assert db_summary.agency_phone_number == resp_summary["agency_phone_number"]
    assert db_summary.agency_contact_description == resp_summary["agency_contact_description"]
    assert db_summary.agency_email_address == resp_summary["agency_email_address"]
    assert (
        db_summary.agency_email_address_description
        == resp_summary["agency_email_address_description"]
    )

    assert set(db_summary.funding_instruments) == set(resp_summary["funding_instruments"])
    assert set(db_summary.funding_categories) == set(resp_summary["funding_categories"])
    assert set(db_summary.applicant_types) == set(resp_summary["applicant_types"])


def validate_assistance_listings(
    db_assistance_listings: list[OpportunityAssistanceListing], resp_listings: list[dict]
) -> None:
    # In order to compare this list, sort them both the same and compare from there
    db_assistance_listings.sort(key=lambda a: (a.assistance_listing_number, a.program_title))
    resp_listings.sort(key=lambda a: (a["assistance_listing_number"], a["program_title"]))

    assert len(db_assistance_listings) == len(resp_listings)
    for db_assistance_listing, resp_listing in zip(
        db_assistance_listings, resp_listings, strict=True
    ):
        assert (
            db_assistance_listing.assistance_listing_number
            == resp_listing["assistance_listing_number"]
        )
        assert db_assistance_listing.program_title == resp_listing["program_title"]


def validate_search_pagination(
    search_response: dict,
    search_request: dict,
    expected_total_pages: int,
    expected_total_records: int,
    expected_response_record_count: int,
):
    pagination_info = search_response["pagination_info"]
    assert pagination_info["page_offset"] == search_request["pagination"]["page_offset"]
    assert pagination_info["page_size"] == search_request["pagination"]["page_size"]
    assert pagination_info["order_by"] == search_request["pagination"]["order_by"]
    assert pagination_info["sort_direction"] == search_request["pagination"]["sort_direction"]

    assert pagination_info["total_pages"] == expected_total_pages
    assert pagination_info["total_records"] == expected_total_records

    searched_opportunities = search_response["data"]
    assert len(searched_opportunities) == expected_response_record_count

    # Verify data is sorted as expected
    reverse = pagination_info["sort_direction"] == "descending"
    resorted_opportunities = sorted(
        searched_opportunities, key=lambda u: u[pagination_info["order_by"]], reverse=reverse
    )
    assert resorted_opportunities == searched_opportunities
