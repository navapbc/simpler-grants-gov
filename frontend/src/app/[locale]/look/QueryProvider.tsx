"use client"

import React, { use } from "react"
import { createContext, useCallback, useContext, useMemo, useState } from 'react';
import { useSearchParams } from "next/navigation";
import { set } from "lodash";

export const QueryContext = createContext<any>({});

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