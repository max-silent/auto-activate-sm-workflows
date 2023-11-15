import logging
import sys

from pydantic import BaseSettings
from pydantic.error_wrappers import ValidationError

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    APP_NAME: str = "customer-user-mgmt"
    API_V1_STR: str = "/v1"


try:
    settings = Settings()
except ValidationError as e:
    logger.exception(e)
    sys.exit(1)
