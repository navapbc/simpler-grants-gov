import { render, waitFor } from "tests/react-utils";

import NewsletterConfirmation from "src/app/[locale]/subscribe/confirmation/page";
import { axe } from "jest-axe";

describe("Newsletter", () => {
  it("passes accessibility scan", async () => {
    const { container } = render(<NewsletterConfirmation />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
