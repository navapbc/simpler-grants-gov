"use client";
import SearchSortyBy from "./SearchSortBy";
import { QueryContext } from "src/app/[locale]/search/QueryProvider";
import { useContext } from "react";

export default function SearchResultsHeader({
  sortby,
  totalFetchedResults,
  queryTerm,
  loading = false,
}: {
  sortby: string | null;
  totalFetchedResults?: string;
  queryTerm?: string | null | undefined;
  loading?: boolean;
}) {
  const { totalResults } = useContext(QueryContext);
  const total = totalFetchedResults || totalResults;
  return (
    <div className="grid-row">
      <h2
        className="tablet-lg:grid-col-fill margin-top-5 tablet-lg:margin-top-2 tablet-lg:margin-bottom-0"
        style={{ opacity: loading ? 0.5 : 1 }}
      >
        {total && <>{total} Opportunities</>}
      </h2>
      <div className="tablet-lg:grid-col-auto">
        <SearchSortyBy
          totalResults={total}
          sortby={sortby}
          queryTerm={queryTerm}
        />
      </div>
    </div>
  );
}
