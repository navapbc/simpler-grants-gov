import BetaAlert from "src/components/BetaAlert";
import Breadcrumbs from "src/components/Breadcrumbs";
import Loading from "src/app/[locale]/search/loading";
import PageSEO from "src/components/PageSEO";
import SearchResultsList from "src/components/search/SearchResultList";
import QueryProvider from "./QueryProvider";
import SearchBar from "src/components/search/SearchBar";
import SearchCallToAction from "src/components/search/SearchCallToAction";
import SearchFilterAccordion from "src/components/search/SearchFilterAccordion/SearchFilterAccordion";
import SearchOpportunityStatus from "src/components/search/SearchOpportunityStatus";
import SearchPagination from "src/components/search/SearchPagination";
import SearchPaginationLoader from "src/components/search/SearchPaginationLoader";
import SearchResultsHeader from "src/components/search/SearchResultsHeader";
import withFeatureFlag from "src/hoc/search/withFeatureFlag";
import { agencyOptions, categoryOptions, eligibilityOptions, fundingOptions } from "src/components/search/SearchFilterAccordion/SearchFilterOptions";
import { convertSearchParamsToProperTypes } from "src/utils/search/convertSearchParamsToProperTypes";
import { getTranslations, unstable_setRequestLocale } from "next-intl/server";
import { Metadata } from "next";
import { useTranslations } from "next-intl";
import { SEARCH_CRUMBS } from "src/constants/breadcrumbs";
import { Suspense } from 'react';

export async function generateMetadata() {
  const t = await getTranslations({ locale: "en" });
  const meta: Metadata = {
    title: t("Search.title"),
    description: t("Index.meta_description"),
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
  sortby?: string;
  status?: string;
  [key: string]: string | undefined;
}

function Search({
  searchParams,
}: {
  searchParams: searchParamsTypes;
}) {
  unstable_setRequestLocale("en");
  const t = useTranslations("Process");
  const convertedSearchParams = convertSearchParamsToProperTypes(searchParams);
  const { agency, category, eligibility, fundingInstrument, page, query, sortby, status } = convertedSearchParams;
 
  if (!('page' in searchParams)) {
    searchParams.page = '1';
  }
  const key = Object.entries(searchParams).join(',');
  const pager1key = Object.entries(searchParams).join('-') + 'pager1';
  const pager2key = Object.entries(searchParams).join('-') + 'pager2';

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
              <SearchResultsHeader sortby={sortby} />
              <div className="usa-prose">
                <Suspense key={pager1key} fallback={<SearchPaginationLoader page={page}/>}>
                  <SearchPagination searchParams={convertedSearchParams} scroll={false} />
                </Suspense>
                <Suspense key={key} fallback={<Loading />}>
                  <SearchResultsList searchParams={convertedSearchParams} />
                </Suspense>
                <Suspense key={pager2key} fallback={<SearchPaginationLoader page={page}/>}>
                  <SearchPagination searchParams={convertedSearchParams} scroll={true}/>
                </Suspense>
              </div>
            </div>
          </div>
        </div>
      </QueryProvider>
    </>
  );
}
export default withFeatureFlag(Search, "showSearchV0");