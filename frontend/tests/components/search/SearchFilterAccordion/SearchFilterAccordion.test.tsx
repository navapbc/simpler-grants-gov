import "@testing-library/jest-dom/extend-expect";

import SearchFilterAccordion, {
  FilterOption,
} from "src/components/search/SearchFilterAccordion/SearchFilterAccordion";
import { fireEvent, render, screen } from "@testing-library/react";

import React from "react";
import { axe } from "jest-axe";

const initialFilterOptions: FilterOption[] = [
  {
    id: "funding-instrument-cooperative_agreement",
    label: "Cooperative Agreement",
    value: "cooperative_agreement",
  },
  {
    id: "funding-instrument-grant",
    label: "Grant",
    value: "grant",
  },
  {
    id: "funding-instrument-procurement_contract",
    label: "Procurement Contract ",
    value: "procurement_contract",
  },
  {
    id: "funding-instrument-other",
    label: "Other",
    value: "other",
  },
];

describe("SearchFilterAccordion", () => {
  const title = "Test Accordion";
  const queryParamKey = "status";

  it("should not have basic accessibility issues", async () => {
    const { container } = render(
      <SearchFilterAccordion
        options={initialFilterOptions}
        title={title}
        queryParamKey={queryParamKey}
        query={new Set()}
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("displays the correct checkbox labels", () => {
    render(
      <SearchFilterAccordion
        options={initialFilterOptions}
        title={title}
        queryParamKey={queryParamKey}
        query={new Set()}
      />,
    );

    expect(screen.getByText("Cooperative Agreement")).toBeInTheDocument();
    expect(screen.getByText("Grant")).toBeInTheDocument();
    expect(screen.getByText("Procurement Contract")).toBeInTheDocument();
    expect(screen.getByText("Other")).toBeInTheDocument();
  });

  it("displays select all and clear all correctly", () => {
    render(
      <SearchFilterAccordion
        options={initialFilterOptions}
        title={title}
        queryParamKey={queryParamKey}
        query={new Set()}
      />,
    );

    const selectAllButton = screen.getByText("Select All");
    expect(selectAllButton).toBeInTheDocument();
    expect(selectAllButton).toBeEnabled();

    const clearAllButton = screen.getByText("Clear All");
    expect(clearAllButton).toBeInTheDocument();
    expect(clearAllButton).toBeDisabled();

    const cooperativeAgreementCheckbox = screen.getByLabelText(
      "Cooperative Agreement",
    );

    // after clicking one of the boxes, both select all and clear all should be enabled
    fireEvent.click(cooperativeAgreementCheckbox);
    expect(selectAllButton).toBeEnabled();
    expect(clearAllButton).toBeEnabled();
  });

  it("has hidden attribute when collapsed", () => {
    render(
      <SearchFilterAccordion
        options={initialFilterOptions}
        title={title}
        queryParamKey={queryParamKey}
        query={new Set()}
      />,
    );

    const accordionToggleButton = screen.getByTestId(
      "accordionButton_funding-instrument-filter-status",
    );
    const contentDiv = screen.getByTestId(
      "accordionItem_funding-instrument-filter-status",
    );
    expect(contentDiv).toHaveAttribute("hidden");

    // Toggle the accordion and the hidden attribute should be removed
    fireEvent.click(accordionToggleButton);
    expect(contentDiv).not.toHaveAttribute("hidden");
  });

  it("checks boxes correctly and updates count", () => {
    render(
      <SearchFilterAccordion
        options={initialFilterOptions}
        title={title}
        queryParamKey={queryParamKey}
        query={new Set()}
      />,
    );

    const cooperativeAgreementCheckbox = screen.getByLabelText(
      "Cooperative Agreement",
    );
    fireEvent.click(cooperativeAgreementCheckbox);

    const grantCheckbox = screen.getByLabelText("Grant");
    fireEvent.click(grantCheckbox);

    // Verify the count updates to 2
    const countSpan = screen.getByText("2", {
      selector: ".usa-tag.usa-tag--big.radius-pill.margin-left-1",
    });
    expect(countSpan).toBeInTheDocument();

    // Verify the checkboxes are checked
    expect(cooperativeAgreementCheckbox).toBeChecked();
    expect(grantCheckbox).toBeChecked();
  });
});
