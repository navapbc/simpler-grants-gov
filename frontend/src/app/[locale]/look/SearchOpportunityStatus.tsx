"use client";

import { useContext, useEffect, useState } from "react";

import { Checkbox } from "@trussworks/react-uswds";
import { useDebouncedCallback } from "use-debounce";
import { sendGAEvent } from "@next/third-parties/google";
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { useSearchParamUpdater } from "src/hooks/useSearchParamUpdater";
import { QueryContext } from "./QueryProvider";

interface StatusOption {
  id: string;
  label: string;
  value: string;
}

interface SearchOpportunityStatusProps {
  selectedStatuses: string;
}

const statusOptions: StatusOption[] = [
  { id: "status-forecasted", label: "Forecasted", value: "forecasted" },
  { id: "status-posted", label: "Posted", value: "posted" },
  { id: "status-closed", label: "Closed", value: "closed" },
  { id: "status-archived", label: "Archived", value: "archived" },
];

// Wait a half-second before updating query params
// and submitting the form
// const SEARCH_OPPORTUNITY_STATUS_DEBOUNCE_TIME = 500;

const SearchOpportunityStatus: React.FC<SearchOpportunityStatusProps> = ({
  selectedStatuses,
}) => {
  const { queryTerm } = useContext(QueryContext);

  const searchParams = useSearchParams() || undefined;
  const pathname = usePathname() || "";
  const router = useRouter();
  console.log("queryTerm:", queryTerm, "vs. query:", queryTerm);
  console.log("statuses", selectedStatuses)

  const handleCheck = (statusValue: string, isChecked: boolean) => {
    const params = new URLSearchParams(searchParams);
    console.log(isChecked)
    if (statusValue) {
      params.set('status', statusValue);
    } else {
      params.delete('status');
    }
    if (queryTerm) {
      params.set('query', queryTerm);
    } else {
      params.delete('query');
    }
    sendGAEvent("event", "search", { status: statusValue });
    router.replace(`${pathname}?${params.toString()}`);
  };

  return (
    <>
      <h2 className="margin-bottom-1 font-sans-xs">Opportunity status</h2>
      <div className="grid-row flex-wrap">
        {statusOptions.map((option) => (
          <div key={option.id} className="grid-col-6 padding-right-1">
            <Checkbox
              id={option.id}
              name={option.id}
              label={option.label}
              tile={true}
              onChange={(e) => handleCheck(option.value, e.target.checked)}
             //  checked={selectedStatuses?.has(option.value)}
            />
          </div>
        ))}
      </div>
    </>
  );
};

export default SearchOpportunityStatus;
