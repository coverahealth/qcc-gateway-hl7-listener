from typing import ClassVar
from pydantic_settings import BaseSettings

from enum import Enum

class QueueType(str, Enum):
    NATS = "NATS"
    SQS = "SQS"


class Settings(BaseSettings):
    HL7_MLLP_HOST: str
    HL7_MLLP_PORT: int
    OUTBOUND_QUEUE_TYPE: QueueType = QueueType.NATS
    LOG_LEVEL: str = "INFO"

    _instance: ClassVar["Settings"] = None

    @classmethod
    def get_settings(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


settings: Settings = Settings.get_settings()