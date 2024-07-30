"use client";

import { useContext } from "react";

import { Checkbox } from "@trussworks/react-uswds";
// import { useDebouncedCallback } from "use-debounce";
import { QueryContext } from "./QueryProvider";
import { useSearchParamUpdater2 } from "src/hooks/useSearchParamUpdater";

interface StatusOption {
  id: string;
  label: string;
  value: string;
}

interface SearchOpportunityStatusProps {
  selectedStatuses: Set<string>;
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

export default function SearchOpportunityStatus({ selectedStatuses }: SearchOpportunityStatusProps) {
  const { queryTerm } = useContext(QueryContext);
  const { updateQueryParams   } = useSearchParamUpdater2();

  const handleCheck = (statusValue: string, isChecked: boolean) => {
    const updatedStatuses = new Set(selectedStatuses);
    isChecked
      ? updatedStatuses.add(statusValue)
      : updatedStatuses.delete(statusValue);
    const key = "status";
    updateQueryParams(updatedStatuses, key, queryTerm);
  };

  return (
    <>
      <h2 className="margin-bottom-1 font-sans-xs">Opportunity status</h2>
      <div className="grid-row flex-wrap">
        {statusOptions.map((option) => { 
          return (
            <div key={option.id} className="grid-col-6 padding-right-1">
              <Checkbox
                id={option.id}
                name={option.id}
                label={option.label}
                tile={true}
                onChange={(e) => handleCheck(option.value, e.target.checked)}
                checked={selectedStatuses.has(option.value)}
                />
            </div>
        )})}
      </div>
    </>
  );
}