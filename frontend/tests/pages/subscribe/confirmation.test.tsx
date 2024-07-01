import { render, waitFor } from "tests/react-utils";

import SubscribeConfirmation from "src/app/[locale]/subscribe/confirmation/page";
import { axe } from "jest-axe";

describe("Subscribe", () => {
  it("passes accessibility scan", async () => {
    const { container } = render(<SubscribeConfirmation />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
