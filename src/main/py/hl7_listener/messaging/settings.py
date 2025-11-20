from typing import ClassVar, Optional
from pydantic import  AnyUrl
from pydantic_settings import  BaseSettings

from hl7_listener.settings import (
    QueueType,
    settings as settings_
)

import hl7_listener.messaging.cloud_messaging as _cloud_messaging
import hl7_listener.messaging.nats as _nats


class CloudMessagingSettings(BaseSettings):
    OUTBOUND_QUEUE_NAME: Optional[str] = None
    MSG_NAMESPACE:Optional[str] = None

    _instance: ClassVar["CloudMessagingSettings"] = None

    @classmethod
    def get_settings(cls) -> "CloudMessagingSettings":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class NATSSettings(BaseSettings):
    NATS_OUTGOING_SUBJECT: str = "HL7.MESSAGES"
    NATS_SERVER_URL: Optional[str] = None
    PILOT_MODE: bool = False

    _instance: ClassVar["NATSSettings"] = None

    @classmethod
    def get_settings(cls) -> "NATSSettings":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


MESSAGER_CONFIG_MAP = {
    QueueType.NATS: {"settings": NATSSettings.get_settings(), "messager": _nats.NATSMessager},
    QueueType.CLOUD: {"settings": CloudMessagingSettings.get_settings(), "messager": _cloud_messaging.CloudMessager}
}


settings = MESSAGER_CONFIG_MAP[settings_.OUTBOUND_QUEUE_TYPE]["settings"]
messager = MESSAGER_CONFIG_MAP[settings_.OUTBOUND_QUEUE_TYPE]["messager"]()