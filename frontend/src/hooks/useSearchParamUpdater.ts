"use client";

import { sendGAEvent } from "@next/third-parties/google";
import { useSearchParams, usePathname, useRouter } from 'next/navigation';


export function useSearchParamUpdater2() {
  const searchParams = useSearchParams() || undefined;
  const pathname = usePathname() || "";
  const router = useRouter();
  const params = new URLSearchParams(searchParams);

  const updateQueryParams = (
    queryParamValue: string | Set<string>,
    key: string,
    queryTerm: string | null | undefined,
  ) => {
    
    const finalQueryParamValue =
      queryParamValue instanceof Set
        ? Array.from(queryParamValue).join(",")
        : queryParamValue;

    if (finalQueryParamValue) {
      params.set(key, finalQueryParamValue);
    } else {
      params.delete(key);
    }
    if (queryTerm) {
      params.set('query', queryTerm);
    } else {
      params.delete('query');
    } 

    sendGAEvent("event", "search", { key: finalQueryParamValue });
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  }

  return {
    updateQueryParams
  };
}

export function useSearchParamUpdater() {
  const pathname = usePathname() || "";

  // Singular string-type param updates include: search input, dropdown, and page numbers
  // Multi/Set-type param updates include filters: Opportunity Status, Funding Instrument, Eligibility, Agency, Category
  const updateQueryParams = (
    queryParamValue: string | Set<string>,
    key: string,
  ) => {
    // TODO (#1518): Next's useSearchParams was causing issues. document.location.search
    // seems to work better when calling from the form submit. Some follow up work
    // to investigate if URLSearchParams(useSearchParams()) can still work.
    const params = new URLSearchParams(document.location.search);

    const finalQueryParamValue =
      queryParamValue instanceof Set
        ? Array.from(queryParamValue).join(",")
        : queryParamValue;

    if (finalQueryParamValue) {
      params.set(key, finalQueryParamValue);
    } else {
      params.delete(key);
    }

    let newPath = `${pathname}?${params.toString()}`;
    newPath = removeURLEncodedCommas(newPath);
    newPath = removeQuestionMarkIfNoParams(params, newPath);

    window.history.pushState({}, "", newPath);
  };

  return {
    updateQueryParams,
  };
}

function removeURLEncodedCommas(newPath: string) {
  return newPath.replaceAll("%2C", ",");
}

// When we remove all query params we also need to remove
// the question mark from the URL
function removeQuestionMarkIfNoParams(
  params: URLSearchParams,
  newPath: string,
) {
  return params.toString() === "" ? newPath.replaceAll("?", "") : newPath;
}