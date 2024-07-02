"use client"

import { Pagination } from "@trussworks/react-uswds";
import { useSearchParamUpdater2 } from "src/hooks/useSearchParamUpdater";
import { useDebouncedCallback } from "use-debounce";
import { QueryContext } from "./QueryProvider";
import { useContext } from "react";

export enum PaginationPosition {
  Top = "topPagination",
  Bottom = "bottomPagination",
}

interface SearchPaginationProps {
  total: number;
  page: number;
  query: any;
}

const MAX_SLOTS = 7;
const DEBOUNCE_TIME = 300;

export default function SearchPaginationItem({ total, page, query }: SearchPaginationProps) {
  const { updateQueryParams   } = useSearchParamUpdater2();
  const { updateTotalPages } = useContext(QueryContext);

  const debouncedUpdate = useDebouncedCallback(
    (page: string) => {
      updateQueryParams(page, "page", query);
    },
    50,
  );
  const clickNext = () => {
    const nextPage = String(page + 1)
    updateTotalPages(String(total))
    debouncedUpdate(nextPage);
  }

  return (
    <>
      <Pagination
        pathname="/look"
        totalPages={total}
        currentPage={page}
        maxSlots={MAX_SLOTS}
        onClickNext={clickNext}
        onClickPrevious={clickNext}
        onClickPageNumber={clickNext}
      />
    </>
  );
}
