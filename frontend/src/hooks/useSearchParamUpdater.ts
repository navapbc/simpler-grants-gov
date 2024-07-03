"use client";

import { sendGAEvent } from "@next/third-parties/google";
import { useSearchParams, usePathname, useRouter } from 'next/navigation';


export function useSearchParamUpdater() {
  const searchParams = useSearchParams() || undefined;
  const pathname = usePathname() || "";
  const router = useRouter();
  const params = new URLSearchParams(searchParams);

  const updateQueryParams = (
    queryParamValue: string | Set<string>,
    key: string,
    queryTerm: string | null | undefined,
    scroll = false,
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
    if (key !== 'page') {
      params.delete('page');
    }

    sendGAEvent("event", "search", { key: finalQueryParamValue });
    let newPath = `${pathname}?${params.toString()}`;
    newPath = removeURLEncodedCommas(newPath);
    newPath = removeQuestionMarkIfNoParams(params, newPath);
    router.push(newPath, { scroll });
  }

  return {
    updateQueryParams
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