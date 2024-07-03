"use server";
import { getSearchFetcher } from "src/services/search/searchfetcher/SearchFetcherUtil";
import { QueryParamData } from "src/services/search/searchfetcher/SearchFetcher";
import SearchPaginationItem from "./SearchPaginationItem";

interface SearchPaginationProps {
  searchParams: QueryParamData;
  scroll: boolean;
}

export default async function SearchPagination({
  searchParams,
  scroll,
}: SearchPaginationProps) {
  const searchFetcher = getSearchFetcher();
  const searchResults = await searchFetcher.fetchOpportunities(searchParams);
  const totalPages = searchResults.pagination_info?.total_pages;
  const totalResults = searchResults.pagination_info?.total_records;

  return (
    <>
      <SearchPaginationItem
        total={totalPages}
        page={searchParams.page}
        query={searchParams.query}
        scroll={scroll}
        totalResults={String(totalResults)}
      />
    </>
  );
}
