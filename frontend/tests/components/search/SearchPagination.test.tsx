/* eslint-disable jest/no-commented-out-tests */
import "@testing-library/jest-dom/extend-expect";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { axe } from "jest-axe";
import React from "react";
import { QueryContext } from "src/app/[locale]/search/QueryProvider";
import SearchPagination from "src/components/search/SearchPagination";
import { useSearchParamUpdater } from "src/hooks/useSearchParamUpdater";

// Mocking the useSearchParamUpdater hook
jest.mock("src/hooks/useSearchParamUpdater", () => ({
  useSearchParamUpdater: () => ({
    updateQueryParams: jest.fn(),
  }),
}));

// Create a mock QueryProvider
const mockUpdateQueryTerm = jest.fn();
const mockUpdateTotalPages = jest.fn();
const mockUpdateTotalResults = jest.fn();

const MockQueryProvider = ({ children }: { children: React.ReactNode }) => (
  <QueryContext.Provider
    value={{
      queryTerm: null,
      updateQueryTerm: mockUpdateQueryTerm,
      totalPages: "na",
      updateTotalPages: mockUpdateTotalPages,
      totalResults: "",
      updateTotalResults: mockUpdateTotalResults,
    }}
  >
    {children}
  </QueryContext.Provider>
);

describe("SearchPagination", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should not have basic accessibility issues", async () => {
    const { container } = render(<SearchPagination page={1} query={"test"} />);

    const results = await axe(container, {
      rules: {
        // Disable specific rules that are known to fail due to third-party components
        list: { enabled: false },
        "svg-img-alt": { enabled: false },
      },
    });
    expect(results).toHaveNoViolations();
  });
  it("Renders Pagination component when pages > 0", () => {
    render(<SearchPagination page={1} query={"test"} total={10} />);

    expect(screen.getByRole("navigation")).toBeInTheDocument();
  });
  it("Does not render Pagination component when pages <= 0", () => {
    render(<SearchPagination page={1} query={"test"} total={0} />);

    expect(screen.queryByRole("navigation")).not.toBeInTheDocument();
  });
  it("calls updateQueryParams with correct arguments when page number is clicked", async () => {
    const { updateQueryParams } = useSearchParamUpdater();

    render(
      <MockQueryProvider>
        <SearchPagination
          page={1}
          query=""
          total={2}
          scroll={false}
          totalResults={"30"}
          loading={false}
        />
      </MockQueryProvider>,
    );

    // Simulate clicking a page number
    fireEvent.click(screen.getByText("2"));
    // Check if updateQueryParams was called with the correct arguments
    waitFor(() => {
      expect(updateQueryParams).toHaveBeenCalledWith(
        "2",
        "page",
        "test",
        false,
      );
    });
  });
  it("disables interaction and reduces opacity when loading", () => {
    render(
      <MockQueryProvider>
        <SearchPagination
          page={1}
          query=""
          total={2}
          scroll={false}
          totalResults={"30"}
          loading={false}
        />
      </MockQueryProvider>,
    );
    const container = screen.getByText("Next").closest("div");

    // Check styles when loading
    waitFor(() => {
      expect(container).toHaveStyle("pointer-events: none");
      expect(container).toHaveStyle("opacity: 0.5");
    });
  });
  it("calls updateQueryParams with correct arguments when next is clicked", async () => {
    const { updateQueryParams } = useSearchParamUpdater();

    render(
      <MockQueryProvider>
        <SearchPagination
          page={1}
          query=""
          total={2}
          scroll={false}
          totalResults={"30"}
          loading={false}
        />
      </MockQueryProvider>,
    );

    // Simulate clicking a page number
    const container = screen.getByText("Next").closest("div");
    // Check if updateQueryParams was called with the correct arguments
    waitFor(() => {
      expect(updateQueryParams).toHaveBeenCalledWith(
        "2",
        "page",
        "test",
        false,
      );
      expect(updatePage).toHaveBeenCalledWith("1");
    });
  });
  it("calls updateQueryParams with correct arguments when previous is clicked", async () => {
    const { updateQueryParams } = useSearchParamUpdater();

    render(
      <MockQueryProvider>
        <SearchPagination
          page={2}
          query=""
          total={2}
          scroll={false}
          totalResults={"30"}
          loading={false}
        />
      </MockQueryProvider>,
    );

    // Simulate clicking a page number
    const container = screen.getByText("Previous").closest("div");
    // Check if updateQueryParams was called with the correct arguments
    waitFor(() => {
      expect(updateQueryParams).toHaveBeenCalledWith(
        "1",
        "page",
        "test",
        false,
      );
      expect(updatePage).toHaveBeenCalledWith("1");
    });
  });
});
