import { fireEvent, render, screen, waitFor } from "tests/react-utils";

import Subscribe from "src/app/[locale]/subscribe/page";
import { axe } from "jest-axe";
import { useRouter } from "next/navigation";
import userEvent from "@testing-library/user-event";

jest.mock("next/navigation");

describe("Subscribe", () => {
  it("renders signup form with a submit button", () => {
    render(<Subscribe />);

    const sendyform = screen.getByTestId("sendy-form");

    expect(sendyform).toBeInTheDocument();
  });

  it("submits the form successfully", async () => {
    const mockRouter = {
      push: jest.fn(), // the component uses `router.push` only
    };
    (useRouter as jest.Mock).mockReturnValue(mockRouter);
    render(<Subscribe />);

    // Mock the fetch function to return a successful response
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: jest.fn().mockResolvedValue({ message: "Success" }),
    });

    // Fill out the form
    await userEvent.type(screen.getByLabelText(/First Name/i), "John");
    await userEvent.type(screen.getByLabelText(/Last Name/i), "Doe");
    await userEvent.type(
      screen.getByLabelText(/Email/i),
      "john.doe@example.com",
    );

    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /subscribe/i }));

    // Wait for the form submission
    await waitFor(() => {
      expect(mockRouter.push).toHaveBeenCalledWith(
        "/newsletter/confirmation/?sendy=Success",
      );
    });
  });

  it("shows alert when recieving an error from Sendy", async () => {
    render(<Subscribe />);

    // Mock the fetch function to return a successful response
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      json: jest.fn().mockResolvedValue({ error: "Already subscribed." }),
    });
    jest.spyOn(global.console, "error");

    // Fill out the form
    await userEvent.type(screen.getByLabelText(/First Name/i), "John");
    await userEvent.type(screen.getByLabelText(/Last Name/i), "Doe");
    await userEvent.type(
      screen.getByLabelText(/Email/i),
      "john.doe@example.com",
    );

    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /subscribe/i }));

    // Wait for the form submission
    await waitFor(() => {
      const alert = screen.getByRole("heading", {
        level: 3,
        name: /You’re already signed up!?/i,
      });
      expect(alert).toBeInTheDocument();
    });
    await waitFor(() => {
      expect(console.error).toHaveBeenCalledWith(
        "client error",
        "Already subscribed.",
      );
    });
  });

  it("prevents the form from submitting when incomplete", async () => {
    render(<Subscribe />);

    // Fill out the form
    await userEvent.type(screen.getByLabelText(/First Name/i), "John");
    await userEvent.type(screen.getByLabelText(/Last Name/i), "Doe");

    // Submit the form
    fireEvent.click(screen.getByRole("button", { name: /subscribe/i }));

    // Wait for the form submission
    await waitFor(() => {
      expect(screen.getByText("Enter your email address.")).toBeInTheDocument();
    });
  });

  it("passes accessibility scan", async () => {
    const { container } = render(<Subscribe />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
