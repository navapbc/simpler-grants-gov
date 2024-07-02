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
import SearchFilterAccordion from "./SearchFilterAccordion/SearchFilterAccordion";
import SearchOpportunityStatus from "./SearchOpportunityStatus";
import SearchPagination from "./SearchPagination";
import { convertSearchParamsToProperTypes } from "src/utils/search/convertSearchParamsToProperTypes";
import { clone } from "lodash";
import { agencyOptions, categoryOptions, eligibilityOptions, fundingOptions } from "./SearchFilterAccordion/SearchFilterOptions"
import { Pagination } from "@trussworks/react-uswds";
import SearchPaginationLoader from "./SearchPaginationLoader";

export async function generateMetadata() {
  const t = await getTranslations({ locale: "en" });
  const meta: Metadata = {
    title: t("Process.page_title"),
    description: t("Process.meta_description"),
  };
  return meta;
}

interface searchParamsTypes {
  agency?: string;
  category?: string;
  eligibility?: string;
  fundingInstrument?: string;
  page?: string;
  query?: string;
  status?: string;
  [key: string]: string | undefined;
}

export default function Look({
  searchParams,
}: {
  searchParams: searchParamsTypes;
}) {
  unstable_setRequestLocale("en");
  const t = useTranslations("Process");
  const convertedSearchParams = convertSearchParamsToProperTypes(searchParams);
  const { agency, category, eligibility, fundingInstrument, page, query, status } = convertedSearchParams;
 
  if (!('page' in searchParams)) {
    searchParams.page = '1';
  }
  const key = Object.entries(searchParams).join(',');
  const keySansPage = Object.entries(searchParams).join('-') + 'page';

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
              <div className="usa-prose">
                <Suspense key={keySansPage} fallback={<SearchPaginationLoader page={page}/>}>
                  <SearchPagination searchParams={convertedSearchParams} />
                </Suspense>
                <Suspense key={key} fallback={<Loading />}>
                  <SearchResultsList searchParams={convertedSearchParams} />
                </Suspense>
              </div>
            </div>
          </div>
        </div>
      </QueryProvider>
    </>
  );
}
