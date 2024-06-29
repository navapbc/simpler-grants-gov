"use client";

import {
  FilterOption,
  SearchFilterAccordion,
} from "./SearchFilterAccordion/SearchFilterAccordion";

export interface SearchFilterFundingInstrumentProps {
  query: Set<string>;
}

const initialFilterOptions: FilterOption[] = [
  {
    id: "funding-instrument-cooperative_agreement",
    label: "Cooperative Agreement",
    value: "cooperative_agreement",
  },
  {
    id: "funding-instrument-grant",
    label: "Grant",
    value: "grant",
  },
  {
    id: "funding-instrument-procurement_contract",
    label: "Procurement Contract ",
    value: "procurement_contract",
  },
  {
    id: "funding-instrument-other",
    label: "Other",
    value: "other",
  },
];

export default function SearchFilterFundingInstrument({
  query,
}: SearchFilterFundingInstrumentProps) {
  console.log('render', query);
  return (
    <SearchFilterAccordion
      options={initialFilterOptions}
      title="Funding instrument"
      queryParamKey="fundingInstrument"
      query={query}
    />
  );
}
