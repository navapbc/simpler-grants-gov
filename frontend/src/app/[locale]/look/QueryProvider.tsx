"use client"

import { createContext, useCallback, useMemo, useState } from 'react';
import { useSearchParams } from "next/navigation";

interface QueryContextParams {
  queryTerm: string | null | undefined;
  updateQueryTerm: (term: string) => void;
}

export const QueryContext = createContext( {} as QueryContextParams );

export default function QueryProvider({
    children,
  }: {
    children: React.ReactNode
  }) {
    const searchParams = useSearchParams() || undefined;
    const defaultTerm = searchParams?.get('query');
    const [queryTerm, setQueryTerm] = useState(defaultTerm);
    console.log("rendering provider:", queryTerm);

    const updateQueryTerm = useCallback((term: string) => {
      setQueryTerm(term);
    }, []);

    const contextValue = useMemo(() => ({
      queryTerm,
      updateQueryTerm
    }), [queryTerm, updateQueryTerm]);

    return (
      <QueryContext.Provider value={contextValue}>
            <h3>Query Provider</h3>
            {children}
      </QueryContext.Provider>
    )
}