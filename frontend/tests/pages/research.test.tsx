import { render, screen, waitFor } from "tests/react-utils";

import { axe } from "jest-axe";
import Research from "src/app/[locale]/research/page";

describe("Research", () => {
  it("renders alert with grants.gov link", () => {
    render(<Research />);

    const alert = screen.getByTestId("alert");
    const link = screen.getByRole("link", { name: /www\.grants\.gov/i });

    expect(alert).toBeInTheDocument();
    expect(link).toHaveAttribute("href", "https://www.grants.gov");
  });

  it("passes accessibility scan", async () => {
    const { container } = render(<Research />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
