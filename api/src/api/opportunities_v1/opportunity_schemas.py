from enum import StrEnum

from src.api.schemas.extension import Schema, fields, validators
from src.api.schemas.response_schema import AbstractResponseSchema, PaginationMixinSchema
from src.api.schemas.search_schema import StrSearchSchemaBuilder
from src.constants.lookup_constants import (
    ApplicantType,
    FundingCategory,
    FundingInstrument,
    OpportunityCategory,
    OpportunityStatus,
)
from src.pagination.pagination_schema import generate_pagination_schema


class SearchResponseFormat(StrEnum):
    JSON = "json"
    CSV = "csv"


class OpportunitySummaryV1Schema(Schema):
    summary_description = fields.String(
        allow_none=True,
        metadata={
            "description": "The summary of the opportunity",
            "example": "This opportunity aims to unravel the mysteries of the universe.",
        },
    )
    is_cost_sharing = fields.Boolean(
        allow_none=True,
        metadata={
            "description": "Whether or not the opportunity has a cost sharing/matching requirement",
        },
    )
    is_forecast = fields.Boolean(
        metadata={
            "description": "Whether the opportunity is forecasted, that is, the information is only an estimate and not yet official",
            "example": False,
        }
    )

    close_date = fields.Date(
        allow_none=True,
        metadata={
            "description": "The date that the opportunity will close - only set if is_forecast=False",
        },
    )
    close_date_description = fields.String(
        allow_none=True,
        metadata={
            "description": "Optional details regarding the close date",
            "example": "Proposals are due earlier than usual.",
        },
    )

    post_date = fields.Date(
        allow_none=True,
        metadata={
            "description": "The date the opportunity was posted",
        },
    )
    archive_date = fields.Date(
        allow_none=True,
        metadata={
            "description": "When the opportunity will be archived",
        },
    )
    # not including unarchive date at the moment

    expected_number_of_awards = fields.Integer(
        allow_none=True,
        metadata={
            "description": "The number of awards the opportunity is expected to award",
            "example": 10,
        },
    )
    estimated_total_program_funding = fields.Integer(
        allow_none=True,
        metadata={
            "description": "The total program funding of the opportunity in US Dollars",
            "example": 10_000_000,
        },
    )
    award_floor = fields.Integer(
        allow_none=True,
        metadata={
            "description": "The minimum amount an opportunity would award",
            "example": 10_000,
        },
    )
    award_ceiling = fields.Integer(
        allow_none=True,
        metadata={
            "description": "The maximum amount an opportunity would award",
            "example": 100_000,
        },
    )

    additional_info_url = fields.String(
        allow_none=True,
        metadata={
            "description": "A URL to a website that can provide additional information about the opportunity",
            "example": "grants.gov",
        },
    )
    additional_info_url_description = fields.String(
        allow_none=True,
        metadata={
            "description": "The text to display for the additional_info_url link",
            "example": "Click me for more info",
        },
    )

    forecasted_post_date = fields.Date(
        allow_none=True,
        metadata={
            "description": "Forecasted opportunity only. The date the opportunity is expected to be posted, and transition out of being a forecast"
        },
    )
    forecasted_close_date = fields.Date(
        allow_none=True,
        metadata={
            "description": "Forecasted opportunity only. The date the opportunity is expected to be close once posted."
        },
    )
    forecasted_close_date_description = fields.String(
        allow_none=True,
        metadata={
            "description": "Forecasted opportunity only. Optional details regarding the forecasted closed date.",
            "example": "Proposals will probably be due on this date",
        },
    )
    forecasted_award_date = fields.Date(
        allow_none=True,
        metadata={
            "description": "Forecasted opportunity only. The date the grantor plans to award the opportunity."
        },
    )
    forecasted_project_start_date = fields.Date(
        allow_none=True,
        metadata={
            "description": "Forecasted opportunity only. The date the grantor expects the award recipient should start their project"
        },
    )
    fiscal_year = fields.Integer(
        allow_none=True,
        metadata={
            "description": "Forecasted opportunity only. The fiscal year the project is expected to be funded and launched"
        },
    )

    funding_category_description = fields.String(
        allow_none=True,
        metadata={
            "description": "Additional information about the funding category",
            "example": "Economic Support",
        },
    )
    applicant_eligibility_description = fields.String(
        allow_none=True,
        metadata={
            "description": "Additional information about the types of applicants that are eligible",
            "example": "All types of domestic applicants are eligible to apply",
        },
    )

    agency_code = fields.String(
        allow_none=True,
        metadata={
            "description": "The agency who owns the opportunity",
            "example": "US-ABC",
        },
    )
    agency_name = fields.String(
        allow_none=True,
        metadata={
            "description": "The name of the agency who owns the opportunity",
            "example": "US Alphabetical Basic Corp",
        },
    )
    agency_phone_number = fields.String(
        allow_none=True,
        metadata={
            "description": "The phone number of the agency who owns the opportunity",
            "example": "123-456-7890",
        },
    )
    agency_contact_description = fields.String(
        allow_none=True,
        metadata={
            "description": "Information regarding contacting the agency who owns the opportunity",
            "example": "For more information, reach out to Jane Smith at agency US-ABC",
        },
    )
    agency_email_address = fields.String(
        allow_none=True,
        metadata={
            "description": "The contact email of the agency who owns the opportunity",
            "example": "fake_email@grants.gov",
        },
    )
    agency_email_address_description = fields.String(
        allow_none=True,
        metadata={
            "description": "The text for the link to the agency email address",
            "example": "Click me to email the agency",
        },
    )

    funding_instruments = fields.List(fields.Enum(FundingInstrument))
    funding_categories = fields.List(fields.Enum(FundingCategory))
    applicant_types = fields.List(fields.Enum(ApplicantType))

    created_at = fields.DateTime(
        metadata={"description": "When the opportunity summary was created"}
    )
    updated_at = fields.DateTime(
        metadata={"description": "When the opportunity summary was last updated"}
    )


class OpportunityAssistanceListingV1Schema(Schema):
    program_title = fields.String(
        allow_none=True,
        metadata={
            "description": "The name of the program, see https://sam.gov/content/assistance-listings for more detail",
            "example": "Space Technology",
        },
    )
    assistance_listing_number = fields.String(
        allow_none=True,
        metadata={
            "description": "The assistance listing number, see https://sam.gov/content/assistance-listings for more detail",
            "example": "43.012",
        },
    )


class OpportunityV1Schema(Schema):
    opportunity_id = fields.Integer(
        metadata={"description": "The internal ID of the opportunity", "example": 12345},
    )

    opportunity_number = fields.String(
        allow_none=True,
        metadata={"description": "The funding opportunity number", "example": "ABC-123-XYZ-001"},
    )
    opportunity_title = fields.String(
        allow_none=True,
        metadata={
            "description": "The title of the opportunity",
            "example": "Research into conservation techniques",
        },
    )
    agency = fields.String(
        allow_none=True,
        metadata={"description": "The agency who created the opportunity", "example": "US-ABC"},
    )

    category = fields.Enum(
        OpportunityCategory,
        allow_none=True,
        metadata={
            "description": "The opportunity category",
            "example": OpportunityCategory.DISCRETIONARY,
        },
    )
    category_explanation = fields.String(
        allow_none=True,
        metadata={
            "description": "Explanation of the category when the category is 'O' (other)",
            "example": None,
        },
    )

    opportunity_assistance_listings = fields.List(
        fields.Nested(OpportunityAssistanceListingV1Schema())
    )
    summary = fields.Nested(OpportunitySummaryV1Schema())

    opportunity_status = fields.Enum(
        OpportunityStatus,
        metadata={
            "description": "The current status of the opportunity",
            "example": OpportunityStatus.POSTED,
        },
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OpportunitySearchFilterV1Schema(Schema):
    funding_instrument = fields.Nested(
        StrSearchSchemaBuilder("FundingInstrumentFilterV1Schema")
        .with_one_of(allowed_values=FundingInstrument)
        .build()
    )
    funding_category = fields.Nested(
        StrSearchSchemaBuilder("FundingCategoryFilterV1Schema")
        .with_one_of(allowed_values=FundingCategory)
        .build()
    )
    applicant_type = fields.Nested(
        StrSearchSchemaBuilder("ApplicantTypeFilterV1Schema")
        .with_one_of(allowed_values=ApplicantType)
        .build()
    )
    opportunity_status = fields.Nested(
        StrSearchSchemaBuilder("OpportunityStatusFilterV1Schema")
        .with_one_of(allowed_values=OpportunityStatus)
        .build()
    )
    agency = fields.Nested(
        StrSearchSchemaBuilder("AgencyFilterV1Schema")
        .with_one_of(example="USAID", minimum_length=2)
        .build()
    )


class OpportunityFacetV1Schema(Schema):
    opportunity_status = fields.Dict(
        keys=fields.String(),
        values=fields.Integer(),
        metadata={
            "description": "The counts of opportunity_status values in the full response",
            "example": {"posted": 1, "forecasted": 2},
        },
    )
    applicant_type = fields.Dict(
        keys=fields.String(),
        values=fields.Integer(),
        metadata={
            "description": "The counts of applicant_type values in the full response",
            "example": {
                "state_governments": 3,
                "county_governments": 2,
                "city_or_township_governments": 1,
            },
        },
    )
    funding_instrument = fields.Dict(
        keys=fields.String(),
        values=fields.Integer(),
        metadata={
            "description": "The counts of funding_instrument values in the full response",
            "example": {"cooperative_agreement": 4, "grant": 3},
        },
    )
    funding_category = fields.Dict(
        keys=fields.String(),
        values=fields.Integer(),
        metadata={
            "description": "The counts of funding_category values in the full response",
            "example": {"recovery_act": 2, "arts": 3, "agriculture": 5},
        },
    )
    agency = fields.Dict(
        keys=fields.String(),
        values=fields.Integer(),
        metadata={
            "description": "The counts of agency values in the full response",
            "example": {"USAID": 4, "ARPAH": 3},
        },
    )


class OpportunitySearchRequestV1Schema(Schema):
    query = fields.String(
        metadata={
            "description": "Query string which searches against several text fields",
            "example": "research",
        },
        validate=[validators.Length(min=1, max=100)],
    )

    filters = fields.Nested(OpportunitySearchFilterV1Schema())

    pagination = fields.Nested(
        generate_pagination_schema(
            "OpportunityPaginationV1Schema",
            [
                "relevancy",
                "opportunity_id",
                "opportunity_number",
                "opportunity_title",
                "post_date",
                "close_date",
                "agency_code",
            ],
        ),
        required=True,
    )

    format = fields.Enum(
        SearchResponseFormat,
        load_default=SearchResponseFormat.JSON,
        metadata={
            "description": "The format of the response",
            "default": SearchResponseFormat.JSON,
        },
    )


class OpportunityGetResponseV1Schema(AbstractResponseSchema):
    data = fields.Nested(OpportunityV1Schema())


class OpportunitySearchResponseV1Schema(AbstractResponseSchema, PaginationMixinSchema):
    data = fields.Nested(OpportunityV1Schema(many=True))

    facet_counts = fields.Nested(
        OpportunityFacetV1Schema(),
        metadata={"description": "Counts of filter/facet values in the full response"},
    )
