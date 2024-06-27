import { render, screen } from "tests/react-utils";

import { ExternalRoutes } from "src/constants/routes";
import Footer from "src/components/Footer";

describe("Footer", () => {
  it("Renders without errors", () => {
    render(<Footer />);
    const footer = screen.getByTestId("footer");
    expect(footer).toBeInTheDocument();
  });

  it("Renders social links", () => {
    render(<Footer />);

    const twitter = screen.getByTitle("Twitter");
    const youtube = screen.getByTitle("YouTube");
    const github = screen.getByTitle("Github");
    const rss = screen.getByTitle("RSS");
    const subscribe = screen.getByTitle("Subscribe");
    const blog = screen.getByTitle("Blog");

    expect(twitter).toBeInTheDocument();
    expect(twitter).toHaveAttribute("href", ExternalRoutes.GRANTS_TWITTER);

    expect(youtube).toBeInTheDocument();
    expect(youtube).toHaveAttribute("href", ExternalRoutes.GRANTS_YOUTUBE);

    expect(github).toBeInTheDocument();
    expect(github).toHaveAttribute("href", ExternalRoutes.GITHUB_REPO);

    expect(rss).toBeInTheDocument();
    expect(rss).toHaveAttribute("href", ExternalRoutes.GRANTS_RSS);

    expect(subscribe).toBeInTheDocument();
    expect(subscribe).toHaveAttribute("href", ExternalRoutes.GRANTS_SUBSCRIBE);

    expect(blog).toBeInTheDocument();
    expect(blog).toHaveAttribute("href", ExternalRoutes.GRANTS_BLOG);
  });
});
