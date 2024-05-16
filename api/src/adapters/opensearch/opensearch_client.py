from typing import Any

import opensearchpy

from src.adapters.opensearch.opensearch_config import OpensearchConfig, get_opensearch_config

# More configuration/setup coming in:
# TODO - https://github.com/navapbc/simpler-grants-gov/issues/13



def get_opensearch_client(
    opensearch_config: OpensearchConfig | None = None,
) -> opensearchpy.OpenSearch:
    if opensearch_config is None:
        opensearch_config = get_opensearch_config()

    # See: https://opensearch.org/docs/latest/clients/python-low-level/ for more details
    return opensearchpy.OpenSearch(**_get_connection_parameters(opensearch_config))

def _get_connection_parameters(opensearch_config: OpensearchConfig) -> dict[str, Any]:

    # TODO - we'll want to add the AWS connection params here when we set that up
    # See: https://opensearch.org/docs/latest/clients/python-low-level/#connecting-to-amazon-opensearch-serverless

    return dict(
        hosts=[{"host": opensearch_config.host, "port":opensearch_config.port}],
        http_compress=True,
        use_ssl=opensearch_config.use_ssl,
        verify_certs=opensearch_config.verify_certs,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )