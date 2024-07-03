"use client"

import { Pagination } from "@trussworks/react-uswds";
import { QueryContext } from "../../app/[locale]/search/QueryProvider";
import { useContext } from "react";

interface SearchPaginationProps {
  page: number;
}

const MAX_SLOTS = 7;

export default function SearchPaginationLoader({ page }: SearchPaginationProps) {
  const { totalPages } = useContext(QueryContext);
  const total = totalPages === 'na' ? MAX_SLOTS : totalPages;

  return (
    <div style={{opacity: 1}}>
      <Pagination
        pathname="/look"
        totalPages={Number(total)}
        currentPage={page}
        maxSlots={MAX_SLOTS}
      />
    </div>
  );
}
