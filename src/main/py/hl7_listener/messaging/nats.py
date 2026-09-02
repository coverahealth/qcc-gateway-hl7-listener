from typing import (
    Union,
)

from covera.loglib import (
    configure_get_logger,
    extract_correlation_id_context,
)
from covera.tracelib import traced
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrNoServers

import hl7_listener.messaging.settings as msgr_config
from hl7_listener.messaging.base import MessagingInterface

logger = configure_get_logger()
PILOT_HEADER = {"record_id": "pilot:pilot", "payload_type": "hl7", "trigger": "pilot"}


class NATSMessager(MessagingInterface):

    @traced
    async def connect(self) -> bool:
        """Connect to the NATS jetstream server."""
        self.conn = NATS()
        try:
            await self.conn.connect(msgr_config.settings.NATS_SERVER_URL)
            logger.info(
                "Connected to the NATS server URL",
                logging_code="HL7LLOG006",
                nats_server_url=msgr_config.settings.NATS_SERVER_URL
            )
            return True

        except ErrNoServers as exp:
            logger.error(
                "Error connecting to the NATS server",
                logging_code="HL7LERR002",
                exception=exp
            )
            raise exp

    @traced
    async def send_msg(self, msg: Union[str, bytes]) -> None:
        """Synchronously (no callback or async ACK) send the input message to the NATS
        configured Subject.

        Note: An Exception will result if the send times out or fails for other reasons.
        """
        assert isinstance(msg, (str, bytes))

        to_send = msg
        if isinstance(msg, str):
            to_send = msg.encode()

        logger.info("Sending message to the NATS JetStream server", logging_code="HL7LLOG007")

        headers = {
            "payload_type": "hl7",
        }

        correlation_id = extract_correlation_id_context()
        if correlation_id:
            headers["correlation_id"] = correlation_id

        if msgr_config.settings.PILOT_MODE:
            headers.update(PILOT_HEADER)

        kwargs = {
            "subject": msgr_config.settings.NATS_OUTGOING_SUBJECT,
            "payload": to_send,
            "timeout": 10,
            "headers": headers,
        }

        send_response = await self.conn.request(**kwargs)
        logger.info(
            "Response from NATS request for sending an HL7 message",
            logging_code="HL7LLOG008",
            send_response=send_response
        )
