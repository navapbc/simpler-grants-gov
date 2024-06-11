from typing import Any

from marshmallow import post_load

from src.api.feature_flags.feature_flag import FeatureFlag
from src.api.feature_flags.feature_flag_config import FeatureFlagConfig, get_feature_flag_config
from src.api.schemas.extension import Schema, fields
from src.api.schemas.response_schema import AbstractResponseSchema, PaginationMixinSchema
from src.constants.lookup_constants import OpportunityCategoryLegacy
from src.pagination.pagination_schema import PaginationSchema, generate_sorting_schema


class OpportunityV0Schema(Schema):
    # NOTE: This schema is named with V0 as schema names need to be globally unique

    opportunity_id = fields.Integer(
        dump_only=True,
        metadata={"description": "The internal ID of the opportunity", "example": 12345},
    )

    opportunity_number = fields.String(
        metadata={"description": "The funding opportunity number", "example": "ABC-123-XYZ-001"}
    )
    opportunity_title = fields.String(
        metadata={
            "description": "The title of the opportunity",
            "example": "Research into conservation techniques",
        }
    )
    agency = fields.String(
        metadata={"description": "The agency who created the opportunity", "example": "US-ABC"}
    )

    category = fields.Enum(
        OpportunityCategoryLegacy,
        metadata={
            "description": "The opportunity category",
            "example": OpportunityCategoryLegacy.DISCRETIONARY,
        },
    )
    category_explanation = fields.String(
        metadata={
            "description": "Explanation of the category when the category is 'O' (other)",
            "example": None,
        }
    )

    revision_number = fields.Integer(
        metadata={
            "description": "The current revision number of the opportunity, counting starts at 0",
            "example": 0,
        }
    )
    modified_comments = fields.String(
        metadata={
            "description": "Details regarding what modification was last made",
            "example": None,
        }
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OpportunitySearchSchema(Schema):
    opportunity_title = fields.String(
        metadata={
            "description": "The title of the opportunity to search for",
            "example": "research",
        }
    )
    category = fields.Enum(
        OpportunityCategoryLegacy,
        metadata={
            "description": "The opportunity category to search for",
            "example": OpportunityCategoryLegacy.DISCRETIONARY,
        },
    )

    sorting = fields.Nested(
        generate_sorting_schema(
            "OpportunitySortingSchema",
            order_by_fields=[
                "opportunity_id",
                "agency",
                "opportunity_number",
                "created_at",
                "updated_at",
            ],
        )(),
        required=True,
    )
    paging = fields.Nested(PaginationSchema(), required=True)


class OpportunitySearchHeaderSchema(Schema):
    # Header field: FF-Enable-Opportunity-Log-Msg
    enable_opportunity_log_msg = fields.Boolean(
        data_key=FeatureFlag.ENABLE_OPPORTUNITY_LOG_MSG.get_header_name(),
        metadata={"description": "Whether to log a message in the opportunity endpoint"},
    )

    @post_load
    def post_load(self, data: dict, **kwargs: Any) -> FeatureFlagConfig:
        """
        Merge the default feature flag values with any header overrides.

        Then return the FeatureFlagConfig object rather than a dictionary.
        """
        feature_flag_config = get_feature_flag_config()

        enable_opportunity_log_msg = data.get("enable_opportunity_log_msg", None)
        if enable_opportunity_log_msg is not None:
            feature_flag_config.enable_opportunity_log_msg = enable_opportunity_log_msg

        return feature_flag_config


class OpportunityGetResponseV0Schema(AbstractResponseSchema):
    data = fields.Nested(OpportunityV0Schema())


class OpportunitySearchResponseV0Schema(AbstractResponseSchema, PaginationMixinSchema):
    data = fields.Nested(OpportunityV0Schema(many=True))
