"use client";

import { Pagination } from "@trussworks/react-uswds";
import { QueryContext } from "src/app/[locale]/search/QueryProvider";
import { useSearchParamUpdater } from "src/hooks/useSearchParamUpdater";
import { useDebouncedCallback } from "use-debounce";
import { useContext } from "react";

export enum PaginationPosition {
  Top = "topPagination",
  Bottom = "bottomPagination",
}

interface SearchPaginationProps {
  total: number;
  page: number;
  query: string | null | undefined;
  scroll: boolean;
  totalResults: string;
}

const MAX_SLOTS = 7;

export default function SearchPaginationItem({
  total,
  page,
  query,
  scroll,
  totalResults,
}: SearchPaginationProps) {
  const { updateQueryParams } = useSearchParamUpdater();
  const { updateTotalPages, updateTotalResults } = useContext(QueryContext);

  // TODO: determine better state management. The results are grabbed on the server but
  // not available to the client components that aren't suspense wrapped.
  updateTotalResults(totalResults);
  const debouncedUpdate = useDebouncedCallback((page: string) => {
    updateQueryParams(page, "page", query, scroll);
  }, 50);

  const updatePage = (page: number) => {
    updateTotalPages(String(total));
    debouncedUpdate(String(page));
  };

  return (
    <>
      <Pagination
        pathname="/search"
        totalPages={total}
        currentPage={page}
        maxSlots={MAX_SLOTS}
        onClickNext={() => updatePage(page + 1)}
        onClickPrevious={() => updatePage(page > 1 ? page - 1 : 0)}
        onClickPageNumber={(event: React.MouseEvent, page: number) =>
          updatePage(page)
        }
      />
    </>
  );
}
