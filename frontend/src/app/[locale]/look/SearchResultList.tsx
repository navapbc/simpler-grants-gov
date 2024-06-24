import SearchErrorAlert from "src/components/search/error/SearchErrorAlert";
import SearchResultsListItem from "src/components/search/SearchResultsListItem";
import { getSearchFetcher } from "src/services/search/searchfetcher/SearchFetcherUtil";
import { ServerSideSearchParams } from "src/types/searchRequestURLTypes";
import { convertSearchParamsToProperTypes } from "src/utils/search/convertSearchParamsToProperTypes";

interface ServerPageProps {
  searchParams: ServerSideSearchParams;
}
export default async function SearchResultsList({ searchParams }: ServerPageProps) {

  const searchFetcher = getSearchFetcher();
  const convertedSearchParams = convertSearchParamsToProperTypes(searchParams);

  const searchResults = await searchFetcher.fetchOpportunities(
    convertedSearchParams,
  );
  const maxPaginationError = null;
  const errors = null;

  if (errors) {
    return <SearchErrorAlert />;
  }

  if (searchResults.data.length === 0) {
    return (
      <div>
        <h2>Your search did not return any results.</h2>
        <ul>
          <li>{"Check any terms you've entered for typos"}</li>
          <li>Try different keywords</li>
          <li>{"Make sure you've selected the right statuses"}</li>
          <li>Try resetting filters or selecting fewer options</li>
        </ul>
      </div>
    );
  }

  return (
    <ul className="usa-list--unstyled">
      {/* TODO #1485: show proper USWDS error  */}
      {maxPaginationError && (
        <h4>
          {
            "You''re trying to access opportunity results that are beyond the last page of data."
          }
        </h4>
      )}
      {searchResults.data.map((opportunity) => (
        <li key={opportunity?.opportunity_id}>
          <SearchResultsListItem
            opportunity={opportunity}
          />
        </li>
      ))}
    </ul>
  );
};