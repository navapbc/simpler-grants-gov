"use client";

import { useContext } from "react";

import { Checkbox } from "@trussworks/react-uswds";
// import { useDebouncedCallback } from "use-debounce";
import { sendGAEvent } from "@next/third-parties/google";
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { QueryContext } from "./QueryProvider";
// import { useSearchParamUpdater } from "src/hooks/useSearchParamUpdater";

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

export default function SearchOpportunityStatus({ selectedStatuses }: SearchOpportunityStatusProps) {
  const { queryTerm } = useContext(QueryContext);

  const searchParams = useSearchParams() || undefined;
  const pathname = usePathname() || "";
  const router = useRouter();
  const statuses = selectedStatuses ? selectedStatuses.split(",") : [];

  const updateAll = (statusValue: string, isChecked: boolean) => {
    const params = new URLSearchParams(searchParams);
    const currentStatus = params.get('status');
    const currentStatuses = currentStatus ? currentStatus.split(',') : [];

    if (!isChecked) {
      const values = currentStatuses.filter(status => status !== statusValue);
      if (values.length) {
        params.set('status', values.join(','));
      }
      else {
        params.delete('status');
      }
    }
    else {
      const status = currentStatus ? `${currentStatus},${statusValue}` : statusValue;
      params.set('status', status);
    }
    if (queryTerm) {
      params.set('query', queryTerm);
    } else {
      params.delete('query');
    }
    
    sendGAEvent("event", "search", { status: statusValue });
    router.replace(`${pathname}?${params.toString()}`);
  }


  const handleCheck = (statusValue: string, isChecked: boolean) => {
    updateAll(statusValue, isChecked);
  };

  return (
    <>
      <h2 className="margin-bottom-1 font-sans-xs">Opportunity status</h2>
      <h2>{queryTerm}</h2>
      <div className="grid-row flex-wrap">
        {statusOptions.map((option) => { 
          const statusChecked = statuses.indexOf(option.value) >= 0;
          return (
            <div key={option.id} className="grid-col-6 padding-right-1">
              <Checkbox
                id={option.id}
                name={option.id}
                label={option.label}
                tile={true}
                onChange={(e) => handleCheck(option.value, e.target.checked)}
                checked={statusChecked}
              />
            </div>
        )})}
      </div>
    </>
  );
}