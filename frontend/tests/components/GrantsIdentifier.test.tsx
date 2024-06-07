import { render, screen } from "tests/react-utils";

import GrantsIdentifier from "src/components/GrantsIdentifier";

describe("Identifier section", () => {
  it("Renders without errors", () => {
    render(<GrantsIdentifier />);
    const identifier = screen.getByTestId("identifier");
    expect(identifier).toBeInTheDocument();
  });
});
