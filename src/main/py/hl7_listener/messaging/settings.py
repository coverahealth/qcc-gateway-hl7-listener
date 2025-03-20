from pydantic import (
    AnyUrl,
    BaseSettings
)

from hl7_listener.settings import (
    QueueType,
    settings as settings_
)

import hl7_listener.messaging.cloud_messaging as _cloud_messaging
import hl7_listener.messaging.nats as _nats


class CloudMessagingSettings(BaseSettings):
    OUTBOUND_QUEUE_NAME: str
    MSG_NAMESPACE:str


class NATSSettings(BaseSettings):
    NATS_OUTGOING_SUBJECT: str = "HL7.MESSAGES"
    NATS_SERVER_URL: str
    PILOT_MODE: bool = False


MESSAGER_CONFIG_MAP = {
    QueueType.NATS: {"settings": NATSSettings, "messager": _nats.NATSMessager},
    QueueType.CLOUD: {"settings": CloudMessagingSettings, "messager": _cloud_messaging.CloudMessager}
}


settings = MESSAGER_CONFIG_MAP[settings_.OUTBOUND_QUEUE_TYPE]["settings"]()
messager = MESSAGER_CONFIG_MAP[settings_.OUTBOUND_QUEUE_TYPE]["messager"]()