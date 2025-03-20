from typing import (
    Union,
)

from covera.loglib import configure_get_logger
from covera.tracelib import traced

import hl7_listener.messaging.settings as msgr_config
from hl7_listener.messaging.base import MessagingInterface
from covera_cloud_integration import create_client,CloudClient,CloudMessage

logger = configure_get_logger()

class CloudMessager(MessagingInterface):

    @traced
    async def connect(self) -> bool:
        pass
    
    @traced
    async def send_msg(self, msg: Union[str, bytes]) -> None:
        """Sends a msg to an cloud messaging queue."""
        assert isinstance(msg, (str, bytes))

        to_send = msg
        if isinstance(msg, bytes):
            to_send = msg.decode()

        logger.info(
            "Sending message to Cloud",
            logging_code="HL7LLOG009",
            outbound_queue_name=msgr_config.settings.OUTBOUND_QUEUE_NAME
        )

        async with create_client(CloudClient.AZURE_ASYNC_SERVICE_BUS,
                                 **{"namespace":msgr_config.settings.MSG_NAMESPACE
                                    }) as client:
            message_to_send = CloudMessage(data=to_send,content_type="text/plain")
            await client.send_message(msgr_config.settings.OUTBOUND_QUEUE_NAME,message_to_send,timeout=5)
            logger.info("Sent message to Cloud", logging_code="HL7LLOG010")
