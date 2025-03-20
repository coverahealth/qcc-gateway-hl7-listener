from pydantic import BaseSettings

from enum import Enum

class QueueType(str, Enum):
    NATS = "NATS"
    CLOUD = "CLOUD"


class Settings(BaseSettings):
    HL7_MLLP_HOST: str
    HL7_MLLP_PORT: int
    OUTBOUND_QUEUE_TYPE: QueueType = QueueType.NATS
    LOG_LEVEL: str = "INFO"


settings = Settings()