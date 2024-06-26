import { NextApiRequest, NextApiResponse } from "next";
import * as nodeFetch from "node-fetch";
import handler, { Data } from "src/pages/api/subscribe";
import { SendySubscribeForm } from "src/types/sendy";

jest.mock("node-fetch");

const fetchMock = nodeFetch as unknown as jest.MockedFunction<typeof fetch>;
globalThis.fetch = fetchMock;

const mockRequest = {
  method: "POST",
  body: JSON.stringify({
    name: "John",
    email: "john@example.com",
  } as SendySubscribeForm),
} as NextApiRequest;

const mockResponse = {
  status: jest.fn().mockReturnThis(),
  json: jest.fn().mockReturnThis(),
  send: jest.fn().mockReturnThis(),
} as unknown as NextApiResponse<Data>;

describe("Your API Route", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should return 405 if method is not POST", async () => {
    await handler(
      { ...mockRequest, method: "GET" } as NextApiRequest,
      mockResponse,
    );
    expect(mockResponse.status).toHaveBeenCalledWith(405);
    expect(mockResponse.json).toHaveBeenCalledWith({
      error: "Method not allowed",
    });
  });

  it("should return 400 if name or email is missing", async () => {
    await handler(
      { ...mockRequest, body: JSON.stringify({}) } as NextApiRequest,
      mockResponse,
    );
    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith({
      error: "Invalid input. Please provide name and email.",
    });
  });

  it("should return 500 if there is an error during subscription", async () => {
    fetchMock.mockRejectedValueOnce(new Error("Some fetch error"));
    jest.spyOn(global.console, "error");
    await handler(mockRequest, mockResponse);
    expect(mockResponse.status).toHaveBeenCalledWith(500);
    expect(mockResponse.json).toHaveBeenCalledWith({
      error: "Internal Server Error",
    });
    expect(console.error).toHaveBeenCalledWith(
      "Error subscribing user:",
      "Some fetch error",
    );
  });

  it("should return 200 if user subscribed successfully", async () => {
    fetchMock.mockResolvedValueOnce({
      ok: true,
      text: jest.fn().mockResolvedValueOnce("1"),
    } as unknown as Response);
    await handler(mockRequest, mockResponse);
    expect(mockResponse.status).toHaveBeenCalledWith(200);
    expect(mockResponse.json).toHaveBeenCalledWith({
      message: "User subscribed successfully.",
    });
  });

  it("should return 400 if there is an error in the subscription response", async () => {
    fetchMock.mockResolvedValueOnce({
      ok: true,
      text: jest.fn().mockResolvedValueOnce("error message"),
    } as unknown as Response);
    await handler(mockRequest, mockResponse);
    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith({ error: "error message" });
  });
});
