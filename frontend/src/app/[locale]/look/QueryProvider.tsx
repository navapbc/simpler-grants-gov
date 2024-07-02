"use client"

import { createContext, useCallback, useMemo, useState } from 'react';
import { useSearchParams } from "next/navigation";

interface QueryContextParams {
  queryTerm: string | null | undefined;
  updateQueryTerm: (term: string) => void;
  totalPages: string | null | undefined;
  updateTotalPages: (page: string) => void;
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
    const [totalPages, setTotalPages] = useState('na');

    const updateQueryTerm = useCallback((term: string) => {
      setQueryTerm(term);
    }, []);

    const updateTotalPages = useCallback((page: string) => {
      setTotalPages(page);
    }, []);
    const contextValue = useMemo(() => ({
      queryTerm,
      updateQueryTerm,
      totalPages,
      updateTotalPages
    }), [queryTerm, updateQueryTerm, totalPages, updateTotalPages]);

    return (
      <QueryContext.Provider value={contextValue}>
        {children}
      </QueryContext.Provider>
    )
}