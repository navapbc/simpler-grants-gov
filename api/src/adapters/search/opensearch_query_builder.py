import typing

from src.pagination.pagination_models import SortDirection


class SearchQueryBuilder:
    def __init__(self) -> None:
        self.page_size = 25
        self.page_number = 1

        self.sort_values: list[dict[str, dict[str, str]]] = []

        self.must: list[dict] = []
        self.filters: list[dict] = []

        self.aggregations: dict[str, dict] = {}

    def pagination(self, page_size: int, page_number: int) -> typing.Self:
        """
        Set the pagination for the search request.

        Note that page number should be the human-readable page number
        and start counting from 1.
        """
        self.page_size = page_size
        self.page_number = page_number
        return self

    def sort_by(self, sort_values: list[typing.Tuple[str, SortDirection]]) -> typing.Self:
        """
        List of tuples of field name + sort direction to sort by. If you wish to sort by the relevancy
        score provide a field name of "relevancy".

        The order of the tuples matters, and the earlier values will take precedence - or put another way
        the first tuple is the "primary sort", the second is the "secondary sort", and so on. If
        all of the primary sort values are unique, then the secondary sorts won't be relevant.

        If this method is not called, no sort info will be added to the request, and OpenSearch
        will internally default to sorting by relevancy score. If there is no scores calculated,
        then the order is likely the IDs of the documents in the index.

        Note that multiple calls to this method will erase any info provided in a prior call.
        """
        for field, sort_direction in sort_values:
            if field == "relevancy":
                field = "_score"

            self.sort_values.append({field: {"order": sort_direction.short_form()}})

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
            {"simple_query_string": {"query": query, "fields": fields, "default_operator": "AND"}}
        )

        return self

    def filter_terms(self, field: str, terms: list) -> typing.Self:
        """
        For a given field, filter to a set of values.

        These filters do not affect the relevancy score, they are purely
        a binary filter on the overall results.
        """
        self.filters.append({"terms": {field: terms}})
        return self

    def aggregation_terms(
        self, aggregation_name: str, field_name: str, size: int = 25, minimum_count: int = 1
    ) -> typing.Self:
        """
        Add a term aggregation to the request. Aggregations are the counts of particular fields in the
        full response and are often displayed next to filters in a search UI.

        Size determines how many different values can be returned.
        Minimum count determines how many occurrences need to occur to include in the response.
            If you pass in 0 for this, then values that don't occur at all in the full result set will be returned.

        see: https://opensearch.org/docs/latest/aggregations/bucket/terms/
        """
        self.aggregations[aggregation_name] = {
            "terms": {"field": field_name, "size": size, "min_doc_count": minimum_count}
        }
        return self

    def build(self) -> dict:
        """
        Build the search request
        """

        # Base request
        page_offset = self.page_size * (self.page_number - 1)
        request: dict[str, typing.Any] = {
            "size": self.page_size,
            "from": page_offset,
            # Always include the scores in the response objects
            # even if we're sorting by non-relevancy
            "track_scores": True,
        }

        # Add sorting if any was provided
        if len(self.sort_values) > 0:
            request["sort"] = self.sort_values

        # Add a bool query
        #
        # The "must" block contains anything relevant to scoring
        # The "filter" block contains filters that don't affect scoring and act
        #       as just binary filters
        #
        # See: https://opensearch.org/docs/latest/query-dsl/compound/bool/
        bool_query = {}
        if len(self.must) > 0:
            bool_query["must"] = self.must

        if len(self.filters) > 0:
            bool_query["filter"] = self.filters

        # Add the query object which wraps the bool query
        query_obj = {}
        if len(bool_query) > 0:
            query_obj["bool"] = bool_query

        if len(query_obj) > 0:
            request["query"] = query_obj

        # Add any aggregations
        # see: https://opensearch.org/docs/latest/aggregations/
        if len(self.aggregations) > 0:
            request["aggs"] = self.aggregations

        return request
