"use client";
import SearchSortyBy from "./SearchSortBy";
import { QueryContext } from "src/app/[locale]/search/QueryProvider";
import { useContext } from "react";

export default function SearchResultsHeader({ sortby }: {sortby: string | null}) {
  const { totalResults, queryTerm } = useContext(QueryContext);
  

  return (
    <div className="grid-row">
      <h2 className="tablet-lg:grid-col-fill margin-top-5 tablet-lg:margin-top-2 tablet-lg:margin-bottom-0">
        {totalResults.length > 0 &&
          <>{totalResults} Opportunities</>
        } 
      </h2>
      <div className="tablet-lg:grid-col-auto">
        <SearchSortyBy sortby={sortby} queryTerm={queryTerm} />
      </div>
    </div>
  );
}