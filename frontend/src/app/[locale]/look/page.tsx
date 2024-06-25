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
    page?: string;
  };
}) {
  unstable_setRequestLocale("en");
  const t = useTranslations("Process");
  const query = searchParams?.query || '';

  return (
    <>
      <PageSEO title={t("page_title")} description={t("meta_description")} />
      <BetaAlert />
      <Breadcrumbs breadcrumbList={SEARCH_CRUMBS} />
      <SearchCallToAction />
      <div className="grid-container">
        <div className="search-bar">
          <SearchBar query={query}/>
        </div>
        <div className="grid-row grid-gap">
          <div className="tablet:grid-col-4">
          </div>
          <div className="tablet:grid-col-8">
            <Suspense key={query} fallback={<Loading />}>
              <SearchResultsList searchParams={searchParams} />
            </Suspense>
          </div>
        </div>
      </div>
    </>
  );
}
