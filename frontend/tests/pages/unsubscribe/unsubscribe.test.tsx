import { render, waitFor } from "tests/react-utils";

import NewsletterUnsubscribe from "src/app/[locale]/unsubscribe/page";
import { axe } from "jest-axe";

describe("Newsletter", () => {
  it("passes accessibility scan", async () => {
    const { container } = render(<NewsletterUnsubscribe />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
