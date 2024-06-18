import "server-only";

import BaseApi from "./BaseApi";

export default class OpportunityListingAPI extends BaseApi {
  get basePath(): string {
    return process.env.API_URL || "";
  }

  get namespace(): string {
    return "opportunities";
  }

  async getOpportunityById(opportunityId: number) {
    const subPath = `${opportunityId}`;
    const response = await this.request(
      "GET",
      this.basePath,
      this.namespace,
      subPath,
    );
    return response;
  }
}
