import typing

SORT_DIRECTION = typing.Literal["asc", "desc"] # TODO - use an enum?

class SearchQueryBuilder:

    def __init__(self) -> None:
        self.page_size = 25
        self.page_number = 1

        self.sort_by = "relevancy_score"
        self.sort_direction: SORT_DIRECTION = "asc"

        self.must = []

        self.filters = []
        self.aggregations = []

    def pagination(self, page_size: int, page_number: int) -> typing.Self:
        """
        Set the pagination for the search request.

        Note that page number should be the human-readable page number
        and start counting from 1.
        """
        self.page_size = page_size
        self.page_number = page_number
        return self

    def sorting(self, sort_by: str, sort_direction: SORT_DIRECTION) -> typing.Self:
        self.sort_by = sort_by
        self.sort_direction = sort_direction
        return self

    def simple_query(self, query: str, fields: list[str]) -> typing.Self:
        """
        Adds a simple_query_string which queries against the provided fields.

        The fields must include the full path to the object, and can include optional suffixes
        to adjust the weighting. For example "opportunity_title^4" would increase any scores
        derived from that field by 4x.

        See: https://opensearch.org/docs/latest/query-dsl/full-text/simple-query-string/
        """
        self.must.append(
            {
                "simple_query_string": {
                    "query": query,
                    "default_operator": "AND",
                    "fields": fields
                }
            }
        )

        return self

    def filter_terms(self, field: str, terms: list[str | int]) -> typing.Self:
        self.filters.append({"terms": {field: terms}})
        return self

    def aggregation_terms(self, aggregation_name: str, field_name: str, size: int = 25) -> typing.Self:
        self.aggregations.append({
            aggregation_name: {
                "terms": {
                    "field": field_name,
                    "size": size
                }
            }
        })
        return self

    def build(self) -> dict:
        page_offset = self.page_size * (self.page_number - 1)


        request = {
            "size": self.page_size,
            "from": page_offset,
            # Always include the scores in the response objects
            # even if we're sorting by non-relevancy
            "track_scores": True
        }

        if self.sort_by != "relevancy_score":
            request["sort"] = [
                {
                    self.sort_by: {
                        "order": self.sort_direction
                    }
                }
            ]

        bool_query = {}

        if len(self.must) > 0:
            bool_query["must"] = self.must

        if len(self.filters) > 0:
            bool_query["filter"] = self.filters

        if len(bool_query) > 0:
            request["bool"] = bool_query

        return request