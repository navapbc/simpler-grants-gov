import logging

from pydantic import Field

from src.util.env_config import PydanticBaseEnvConfig
from pydantic_settings import SettingsConfigDict

logger = logging.getLogger(__name__)


class OpensearchConfig(PydanticBaseEnvConfig):
    model_config = SettingsConfigDict(env_prefix="OPENSEARCH_")

    host: str # OPENSEARCH_HOST
    port: int # OPENSEARCH_PORT
    use_ssl: bool = Field(default=True) # OPENSEARCH_USE_SSL
    verify_certs: bool = Field(default=True) # OPENSEARCH_VERIFY_CERTS



def get_opensearch_config() -> OpensearchConfig:
    opensearch_config = OpensearchConfig()

    logger.info(
        "Constructed opensearch configuration",
        extra={
            "host": opensearch_config.host,
            "port": opensearch_config.port,
            "use_ssl": opensearch_config.use_ssl,
            "verify_certs": opensearch_config.verify_certs
        },
    )

    return opensearch_config
