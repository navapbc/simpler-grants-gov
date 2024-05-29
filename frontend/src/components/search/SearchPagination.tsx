"use client";

import { Pagination } from "@trussworks/react-uswds";
import { useDebouncedCallback } from "use-debounce";
import { useFormStatus } from "react-dom";

export enum PaginationPosition {
  Top = "topPagination",
  Bottom = "bottomPagination",
}

interface SearchPaginationProps {
  showHiddenInput?: boolean; // Only one of the two SearchPagination should have this set
  page: number;
  handlePageChange: (handlePage: number) => void; // managed in useSearchFormState
  paginationRef?: React.RefObject<HTMLInputElement>; // managed in useSearchFormState
  totalPages: number;
  position: PaginationPosition;
  searchResultsLength: number;
}

const MAX_SLOTS = 7;
const DEBOUNCE_TIME = 300;

export default function SearchPagination({
  showHiddenInput,
  page,
  handlePageChange,
  paginationRef,
  totalPages,
  position,
  searchResultsLength,
}: SearchPaginationProps) {
  const { pending } = useFormStatus();

  const debouncedHandlePageChange = useDebouncedCallback((newPage: number) => {
    handlePageChange(newPage);
  }, DEBOUNCE_TIME);

  // If there's no results, don't show pagination
  if (searchResultsLength < 1) {
    return null;
  }

  // When we're in pending state (updates are being requested)
  // hide the bottom pagination
  if (pending && position === PaginationPosition.Bottom) {
    return null;
  }

  return (
    <>
      {showHiddenInput === true && (
        // Allows us to pass a value to server action when updating results
        <input
          type="hidden"
          name="currentPage"
          ref={paginationRef}
          value={page}
          data-testid="hiddenCurrentPage"
        />
      )}
      <Pagination
        pathname="/search"
        totalPages={totalPages}
        currentPage={page}
        maxSlots={MAX_SLOTS}
        onClickNext={() => debouncedHandlePageChange(page + 1)}
        onClickPrevious={() => debouncedHandlePageChange(page - 1)}
        onClickPageNumber={(event: React.MouseEvent, page: number) =>
          debouncedHandlePageChange(page)
        }
      />
    </>
  );
}
