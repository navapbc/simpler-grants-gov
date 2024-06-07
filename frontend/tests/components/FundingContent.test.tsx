import { render, screen } from "tests/react-utils";
import FundingContent from "src/components/content/FundingContent";

describe("Funding Content", () => {
  it("Renders without errors", () => {
    render(<FundingContent />);
    const fundingH2 = screen.getByRole("heading", {
      level: 2,
      name: /Improvements to funding opportunity announcements?/i,
    });

    expect(fundingH2).toBeInTheDocument();
  });
});
