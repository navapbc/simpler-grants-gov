"use client"
import { QueryParamData } from "src/services/search/searchfetcher/SearchFetcher";
import { getSearchFetcher } from "src/services/search/searchfetcher/SearchFetcherUtil";
import SearchPaginationItem from "./SearchPaginationItem";

interface SearchPaginationProps {
  searchParams: QueryParamData;
}

const MAX_SLOTS = 7;
const DEBOUNCE_TIME = 300;

export default async function SearchResults({ searchParams }: SearchPaginationProps) {
  const searchFetcher = getSearchFetcher();
  const searchResults = await searchFetcher.fetchOpportunities(
    searchParams,
  );
  const totalPages = searchResults.pagination_info?.total_pages
  const page = searchParams.page;

  return (
    <>
      <SearchPaginationItem
        totalPages={totalPages}
        page={searchParams.page}
        query={searchParams.query}


//        onClickPrevious={() => debouncedHandlePageChange(page - 1)}
//        onClickPageNumber={(event: React.MouseEvent, page: number) =>
  //        debouncedHandlePageChange(page)
    //    }
      />
    </>
  );
}
