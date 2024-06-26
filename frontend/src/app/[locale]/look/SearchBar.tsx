"use client";

import { Icon } from "@trussworks/react-uswds";
import { sendGAEvent } from "@next/third-parties/google";
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { QueryContext } from "./QueryProvider";
import { useContext } from "react";

interface SearchBarProps {
  query: string;
}

export default function SearchBar({ query }: SearchBarProps) {
  const { queryTerm, updateQueryTerm } = useContext(QueryContext);

  const searchParams = useSearchParams() || undefined;
  const pathname = usePathname() || "";
  const router = useRouter();

  const handleSubmit = () => {
    const params = new URLSearchParams(searchParams);
    if (queryTerm) {
      params.set('query', queryTerm);
    } else {
      params.delete('query');
    }
    sendGAEvent("event", "search", { search_term: queryTerm });
    router.replace(`${pathname}?${params.toString()}`);
  };

  return (
    <div className="margin-top-5 margin-bottom-2">
      <h1>queryTerm: {queryTerm}</h1>
      <label
        htmlFor="query"
        className="font-sans-lg display-block margin-bottom-2"
      >
        <span className="text-bold">Search terms </span>
        <small className="display-inline-block">
          Enter keywords, opportunity numbers, or assistance listing numbers
        </small>
      </label>
      <div className="usa-search usa-search--big" role="search">
        <input
          className="usa-input maxw-none"
          id="query"
          type="search"
          name="query"
          defaultValue={query}
          onChange={(e) => updateQueryTerm(e.target?.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSubmit();
            }
          }}
        />
        <button className="usa-button" type="submit" onClick={handleSubmit}>
          <span className="usa-search__submit-text">Search </span>
          <Icon.Search
            className="usa-search__submit-icon"
            size={4}
            aria-label="Search"
          />
        </button>
      </div>
    </div>
  );
}