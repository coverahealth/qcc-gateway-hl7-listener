from typing import ClassVar, Optional
from pydantic import AnyUrl 
from pydantic_settings import BaseSettings

from hl7_listener.settings import (
    QueueType,
    settings as settings_
)

import hl7_listener.messaging.sqs as _sqs
import hl7_listener.messaging.nats as _nats


class SQSSettings(BaseSettings):
    SQS_OUTBOUND_QUEUE_URL: Optional[AnyUrl] = None

    _instance: ClassVar["SQSSettings"] = None

    @classmethod
    def get_settings(cls) -> "SQSSettings":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class NATSSettings(BaseSettings):
    NATS_OUTGOING_SUBJECT: str = "HL7.MESSAGES"
    NATS_SERVER_URL: str
    PILOT_MODE: bool = False

    _instance: ClassVar["NATSSettings"] = None

    @classmethod
    def get_settings(cls) -> "NATSSettings":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance



MESSAGER_CONFIG_MAP = {
    QueueType.NATS: {"settings": NATSSettings.get_settings(), "messager": _nats.NATSMessager},
    QueueType.SQS: {"settings": SQSSettings.get_settings(), "messager": _sqs.SQSMessager}
}


settings = MESSAGER_CONFIG_MAP[settings_.OUTBOUND_QUEUE_TYPE]["settings"]
messager = MESSAGER_CONFIG_MAP[settings_.OUTBOUND_QUEUE_TYPE]["messager"]