"use client";
import SearchSortyBy from "./SearchSortBy";
import { QueryContext } from "src/app/[locale]/search/QueryProvider";
import { useContext } from "react";
import { useTranslations } from "next-intl";

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
  const gridRowClasses = [
    "tablet-lg:grid-col-fill",
    "margin-top-5",
    "tablet-lg:margin-top-2",
    "tablet-lg:margin-bottom-0",
  ];
  if (loading) gridRowClasses.push("opacity-50");

  const t = useTranslations("Search");

  return (
    <div className="grid-row">
      <h2 className={gridRowClasses.join(" ")}>
        {t("resultsHeader.message", { count: total })}
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
