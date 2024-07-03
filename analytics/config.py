"""Loads configuration variables from settings files and settings files

Dynaconf provides a few valuable features for configuration management:
- Load variables from env vars and files with predictable overrides
- Validate the existence and format of required configs
- Connect with secrets managers like HashiCorp's Vault server
- Load different configs based on environment (e.g. DEV, PROD, STAGING)

For more information visit: https://www.dynaconf.com/
"""

# from dynaconf import Dynaconf, Validator, ValidationError
from pydantic_settings import BaseSettings
from pydantic import Field

class DBSettings(BaseSettings):
     # will load from the DB_HOST env var if it exists, otherwise use the default
     db_host: str = "localhost"

     # Without a default, will error if the env var isn't set
     port: 5432
     user: "app"
     password: "secret123"

# settings = Dynaconf(
#     # set env vars with `export ANALYTICS_FOO=bar`
#     envvar_prefix="ANALYTICS",
#     # looks for config vars in the following files
#     # with vars in .secrets.toml overriding vars in settings.toml
#     settings_files=["settings.toml", ".secrets.toml"],
#     # merge the settings found in all files
#     merge_enabled= True,
#     # add validators for our required config vars
#     validators=[
#         Validator("SLACK_BOT_TOKEN", must_exist=True),
#         Validator("REPORTING_CHANNEL_ID", must_exist=True),
#     ],
# )

# # raises after all possible errors are evaluated
# try:
#     settings.validators.validate_all()
# except ValidationError as error:
#     list_of_all_errors = error.details
#     print(list_of_all_errors)
#     raise
