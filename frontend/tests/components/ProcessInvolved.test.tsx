import { render, screen } from "@testing-library/react";
import ProcessInvolved from "src/pages/content/ProcessInvolved";

describe("Process Content", () => {
  it("Renders without errors", () => {
    render(<ProcessInvolved />);
    const ProcessH1 = screen.getByRole("heading", {
      level: 3,
      name: /Do you have data expertise?/i,
    });

    expect(ProcessH1).toBeInTheDocument();
  });
});