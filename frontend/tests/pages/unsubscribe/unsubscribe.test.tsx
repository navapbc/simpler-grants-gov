import { render, waitFor } from "tests/react-utils";

import Unsubscribe from "src/app/[locale]/unsubscribe/page";
import { axe } from "jest-axe";

describe("Unsubscribe", () => {
  it("passes accessibility scan", async () => {
    const { container } = render(<Unsubscribe />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
