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
import SearchFilterAccordion from "./SearchFilterAccordion/SearchFilterAccordion";
import { convertSearchParamsToProperTypes } from "src/utils/search/convertSearchParamsToProperTypes";

import { agencyOptions, categoryOptions, eligibilityOptions, fundingOptions } from "./SearchFilterAccordion/SearchFilterOptions"

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
    agency?: string;
    category?: string;
    eligibility?: string;
    fundingInstrument?: string;
    page?: string;
    query?: string;
    status?: string;
  };
}) {
  unstable_setRequestLocale("en");
  const t = useTranslations("Process");
  const key = Object.entries(searchParams).join(',')
  const convertedSearchParams = convertSearchParamsToProperTypes(searchParams);
  const { agency, category, eligibility, fundingInstrument, query, status } = convertedSearchParams;

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
                <SearchFilterAccordion
                  options={fundingOptions}
                  title="Funding instrument"
                  queryParamKey="fundingInstrument"
                  query={fundingInstrument}
                />
                <SearchFilterAccordion
                  options={eligibilityOptions}
                  title="Eligibility"
                  queryParamKey="eligibility"
                  query={eligibility}
                />
                <SearchFilterAccordion
                  options={agencyOptions}
                  title="Agency"
                  queryParamKey="agency"
                  query={agency}
                />
                <SearchFilterAccordion
                  options={categoryOptions}
                  title="Category"
                  queryParamKey="category"
                  query={category}
                />
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
