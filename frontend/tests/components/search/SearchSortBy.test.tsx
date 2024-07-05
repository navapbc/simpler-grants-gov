import { fireEvent, render, screen } from "@testing-library/react";

import React from "react";
import SearchSortBy from "src/components/search/SearchSortBy";
import { axe } from "jest-axe";

// Mock the useSearchParamUpdater hook
jest.mock("src/hooks/useSearchParamUpdater", () => ({
  useSearchParamUpdater: () => ({
    updateQueryParams: jest.fn(),
  }),
}));

describe("SearchSortBy", () => {
  it("should not have basic accessibility issues", async () => {
    const { container } = render(
      <SearchSortBy
        totalResults={"10"}
        queryTerm="test"
        sortby="closeDateDesc"
      />,
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("renders correctly with initial query params", () => {
    render(<SearchSortBy totalResults={"10"} queryTerm="test" sortby="" />);

    expect(
      screen.getByDisplayValue("Posted Date (newest)"),
    ).toBeInTheDocument();
  });

  it("updates sort option and submits the form on change", () => {
    const formElement = document.createElement("form");
    const requestSubmitMock = jest.fn();
    formElement.requestSubmit = requestSubmitMock;

    render(<SearchSortBy totalResults={"10"} queryTerm="test" sortby="" />);

    fireEvent.change(screen.getByRole("combobox"), {
      target: { value: "opportunityTitleDesc" },
    });

    expect(
      screen.getByDisplayValue("Opportunity Title (Z to A)"),
    ).toBeInTheDocument();

    expect(requestSubmitMock).toHaveBeenCalled();
  });
});
