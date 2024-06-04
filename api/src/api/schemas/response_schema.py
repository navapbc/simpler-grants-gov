from src.api.schemas.extension import Schema, fields
from src.pagination.pagination_schema import PaginationInfoSchema


class ValidationIssueSchema(Schema):
    type = fields.String(metadata={"description": "The type of error", "example": "invalid"})
    message = fields.String(
        metadata={"description": "The message to return", "example": "Not a valid string."}
    )
    field = fields.String(
        metadata={"description": "The field that failed", "example": "summary.first_name"}
    )


class AbstractResponseSchema(Schema):
    message = fields.String(metadata={"description": "The message to return", "example": "Success"})
    data = fields.MixinField(metadata={"description": "The REST resource object"}, dump_default={})
    status_code = fields.Integer(
        metadata={"description": "The HTTP status code", "example": 200}, dump_default=200
    )


class WarningMixinSchema(Schema):
    warnings = fields.List(
        fields.Nested(ValidationIssueSchema()),
        metadata={
            "description": "A list of warnings - indicating something you may want to be aware of, but did not prevent handling of the request"
        },
        dump_default=[],
    )


class PaginationMixinSchema(Schema):
    pagination_info = fields.Nested(
        PaginationInfoSchema(),
        metadata={"description": "The pagination information for paginated endpoints"},
    )


class ErrorResponseSchema(Schema):
    message = fields.String(metadata={"description": "General description of the error"})
    status_code = fields.Integer(
        metadata={"description": "The HTTP status code of the error", "example": 404}
    )
    errors = fields.List(fields.Nested(ValidationIssueSchema()), dump_default=[])
