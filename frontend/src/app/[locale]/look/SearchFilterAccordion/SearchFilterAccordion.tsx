import { Accordion } from "@trussworks/react-uswds";
import { QueryParamKey } from "src/types/search/searchResponseTypes";
import SearchFilterCheckbox from "./SearchFilterCheckbox";
import SearchFilterSection from "./SearchFilterSection/SearchFilterSection";
import SearchFilterToggleAll from "./SearchFilterToggleAll";
import { QueryContext } from "src/app/[locale]/look/QueryProvider";
import { useSearchParamUpdater2 } from "src/hooks/useSearchParamUpdater";
import { useContext } from "react";

export interface AccordionItemProps {
  title: React.ReactNode | string;
  content: React.ReactNode;
  expanded: boolean;
  id: string;
  headingLevel: "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
  className?: string;
  // handleToggle?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

export interface FilterOption {
  id: string;
  label: string;
  value: string;
  isChecked?: boolean;
  children?: FilterOption[];
}

interface SearchFilterAccordionProps {
  options: FilterOption[];
  title: string; // Title in header of accordion
  query: Set<string>;
  queryParamKey: QueryParamKey; // Ex - In query params, search?{key}=first,second,third
}

export function SearchFilterAccordion({
  options,
  title,
  queryParamKey,
  query,
}: SearchFilterAccordionProps) {
  const { queryTerm } = useContext(QueryContext);
  const { updateQueryParams   } = useSearchParamUpdater2();
  const totalCheckedCount = query.size
  
 
  const getAccordionTitle = () => (
    <>
      {title}
      {!!totalCheckedCount && (
        <span className="usa-tag usa-tag--big radius-pill margin-left-1">
          {totalCheckedCount}
        </span>
      )}
    </>
  );

  // This should just get the current params and push the update like everything else
  const toggleSelectAll = (all: boolean) => {
    // TODO: need to clear this.
    if (all) {

    }
    else {

    }

  }

  const isSectionAllSelected = (options: FilterOption[], params: Set<string>): boolean => {
    return false;
  }

  const isSectionNoneSelected = (options: FilterOption[], params: Set<string>): boolean => {
    return false;
  }

  const toggleOptionChecked = (value: string, isChecked: boolean) => {
    const updated = new Set(query)
    isChecked
      ? updated.add(value)
      : updated.delete(value);
    const key = queryParamKey;
    updateQueryParams(updated, key, queryTerm);
  }

  const isAllSelected = false;
  const isNoneSelected = true;

  const getAccordionContent = () => (
    <>
      <SearchFilterToggleAll
        onSelectAll={() => toggleSelectAll(true)}
        onClearAll={() => toggleSelectAll(false)}
        isAllSelected={isAllSelected}
        isNoneSelected={isNoneSelected}
      />

      <ul className="usa-list usa-list--unstyled">
        {options.map((option) => (
          <li key={option.id}>
            {/* If we have children, show a "section" dropdown, otherwise show just a checkbox */}
            {option.children ? (
              // SearchFilterSection will map over all children of this option
              <SearchFilterSection
                option={option}
                query={query}
                updateCheckedOption={toggleOptionChecked}
                toggleSelectAll={toggleSelectAll}
                accordionTitle={title}
                // TODO: determine from vars
                isSectionAllSelected={isSectionAllSelected(option.children, query)}
                isSectionNoneSelected={isSectionNoneSelected(option.children, query)}
              />
            ) : (
              <SearchFilterCheckbox
                option={option}
                query={query}
                updateCheckedOption={toggleOptionChecked}
                accordionTitle={title}
              />
            )}
          </li>
        ))}
      </ul>
    </>
  );

  const accordionOptions: AccordionItemProps[] = [
    {
      title: getAccordionTitle(),
      content: getAccordionContent(),
      expanded: false,
      id: `funding-instrument-filter-${queryParamKey}`,
      headingLevel: "h2",
    },
  ];

  return (
    <Accordion
      bordered={true}
      items={accordionOptions}
      multiselectable={true}
      className="margin-top-4"
    />
  );
}

export default SearchFilterAccordion;
