import { SEARCH_CRUMBS } from "src/constants/breadcrumbs";

import BetaAlert from "src/components/BetaAlert";
import SearchCallToAction from "src/components/search/SearchCallToAction";
import Breadcrumbs from "src/components/Breadcrumbs";
import PageSEO from "src/components/PageSEO";
import SearchBar from "./SearchBar";
import { Metadata } from "next";
import { useTranslations } from "next-intl";
import { getTranslations, unstable_setRequestLocale } from "next-intl/server";
import { Suspense } from 'react';
import Loading from "src/app/[locale]/search/loading";
import SearchResultsList from "./SearchResultList";
import QueryProvider from "./QueryProvider";
import SearchOpportunityStatus from "./SearchOpportunityStatus";
import SearchFilterFundingInstrument from "./SearchFilterFundingInstrument";
import { convertSearchParamsToProperTypes } from "src/utils/search/convertSearchParamsToProperTypes";

export async function generateMetadata() {
  const t = await getTranslations({ locale: "en" });
  const meta: Metadata = {
    title: t("Process.page_title"),
    description: t("Process.meta_description"),
  };
  return meta;
}

export default function Look({
  searchParams,
}: {
  searchParams: {
    query?: string;
    status?: string;
    fundingInstrument?: string;
    page?: string;
  };
}) {
  unstable_setRequestLocale("en");
  const t = useTranslations("Process");
  const key = Object.entries(searchParams).join(',')
  console.log(searchParams);
  const convertedSearchParams = convertSearchParamsToProperTypes(searchParams);
  const { query, status, fundingInstrument } = convertedSearchParams;
  console.log(convertedSearchParams);
  console.log('wtf')
  return (
    <>
      <PageSEO title={t("page_title")} description={t("meta_description")} />
      <BetaAlert />
      <Breadcrumbs breadcrumbList={SEARCH_CRUMBS} />
      <SearchCallToAction />
      <QueryProvider>
        <div className="grid-container">
          <div className="search-bar">
              <SearchBar query={query}/>
          </div>
          <div className="grid-row grid-gap">
            <div className="tablet:grid-col-4">
                <SearchOpportunityStatus query={status} />
                <SearchFilterFundingInstrument query={fundingInstrument} />

            </div>
            <div className="tablet:grid-col-8">
              <Suspense key={key} fallback={<Loading />}>
                <SearchResultsList searchParams={searchParams} />
              </Suspense>
            </div>
          </div>
        </div>
      </QueryProvider>
    </>
  );
}
