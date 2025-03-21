"""This HL7 MLLP Listener/Receiver Service will do the following:

1) Connect to the configured HL7 MLLP host and then listen for incoming HL7 messages.
2) Received messages will be sent to the configured NATS JetStream server Subject. If the message sent to the
NATS server fails, the process of listening for incomming HL7 messages will halt.

Preconditions:
- HL7 MLLP host and port are available for use.
- NATS JetStream server is running and configured with expected Subject.
"""
import asyncio
import re

import hl7

from covera.tracelib import traced,configure_tracing
from covera.loglib import (
    configure_get_logger,
    logs_inject_correlation_id,
)
from hl7.mllp import start_hl7_server
from hl7_listener.healthcheck import start_health_check_server
from hl7_listener.messaging.settings import (
    settings as messager_settings,
    messager
)
from hl7_listener.settings import settings

logger = configure_get_logger()


def exception_formatter(exception_text: str):
    exception_text = re.sub(r'\"MSH\|.*\"', "<hl7message>", exception_text)
    if "MSH|" in exception_text:
        exception_text = exception_text[:exception_text.indexOf('MSH|')] + ' <message truncated>'
    return exception_text


@traced
async def process_received_hl7_messages(hl7_reader, hl7_writer):
    """This will be called every time a socket connects to the receiver/listener."""
    peername = hl7_writer.get_extra_info("peername")
    logger.info(
        "HL7 Listener connection established",
        logging_code="HL7LLOG002",
        peername=peername
    )
    try:
        # Note: IncompleteReadError can occur if the HL7 message sender ends and fails to
        # close its writer (reader for this function). It results in a empty byte buffer (b'') which
        # causes the IncompleteReadError. This function's hl7_reader.at_eof() will
        # then be True.
        hl7_message = None
        while not hl7_reader.at_eof():
            hl7_message = await hl7_reader.readmessage()
            # This may not be needed since the hl7_mllp sender should fail if the message
            # was not valid hl7 message.
            _parsed = hl7.parse(str(hl7_message))
            _type, _trigger = _parsed['MSH.F9.R1.1'], _parsed['MSH.F9.R1.2']
            
            logger.info(
                "HL7 Listener received a message",
                logging_code="HL7LLOG003",
                type=f"{_type}^{_trigger}")

            await messager.send_msg(msg=str(hl7_message))

            # Send ACK to acknowledge receipt of the message.
            hl7_writer.writemessage(hl7_message.create_ack())
            # The drain() will fail if the hl7 sender does not process the ACK.
            await hl7_writer.drain()

    except hl7.exceptions.ParseException as exp:
        logger.error(
            "Received HL7 message is not a valid",
            logging_code="HL7LERR006",
            peername=peername,
            exception=Exception(exception_formatter(str(exp)))
        )
        # Send ack code Application Reject (AR).
        hl7_writer.writemessage(hl7_message.create_ack(ack_code="AR"))

    except asyncio.IncompleteReadError as exp:
        if hl7_reader.at_eof():
            logger.info(
                "HL7 Listener connection from a sender peer is closing",
                logging_code="HL7LLOG011",
                peername=peername
            )
        else:
            # Unexpected error.
            logger.error(
                "HL7 MLLP Unexpected incomplete message read error",
                loggin_code='HL7LERR004',
                peername=peername,
                exception=Exception(exception_formatter(str(exp)))
            )
            if hl7_message:
                # Send ack code Application Error (AE).
                hl7_writer.writemessage(hl7_message.create_ack(ack_code="AE"))
            else:
                raise Exception(exception_formatter(str(exp)))

    except Exception as exp:
        logger.error(
            "Unknown error during HL7 receive message processing",
            logging_code="HL7LERR007",
            peername=peername,
            exception=Exception(exception_formatter(str(exp)))
        )
        if hl7_message:
            # Send ack code Application Error (AE).
            hl7_writer.writemessage(hl7_message.create_ack(ack_code="AE"))
        else:
            raise Exception(exception_formatter(str(exp)))

    finally:
        if hl7_writer:
            hl7_writer.close()
            await hl7_writer.wait_closed()
        # Note: the message sender will close the hl7_reader (writer from the
        # sender perspective).
        logger.info(
            "HL7 Listener connection closed",
            logging_code="HL7LLOG004",
            peername=peername
        )


async def hl7_receiver():
    """Receive HL7 MLLP messages on the configured host and port."""
    logger.info(f"Starting the hl7 server on {settings.HL7_MLLP_HOST}:{settings.HL7_MLLP_PORT}")
    try:
        async with await start_hl7_server(
                process_received_hl7_messages,  # Callback function.
                host=settings.HL7_MLLP_HOST,
                port=int(settings.HL7_MLLP_PORT),
        ) as hl7_server:
            # Listen forever or until a cancel occurs.
            await hl7_server.serve_forever()

    except asyncio.CancelledError:
        # Cancel errors are expected.
        logger.info(
            "HL7 Listener was cancelled. This is not considered an error",
            logging_code="HL7LLOG005"
        )
        pass

    except Exception as exp:
        logger.error(
            "HL7 MLLP Receiver encountered exception",
            logging_code="HL7LERR005",
            exception=Exception(exception_formatter(str(exp)))
        )
        raise Exception(exception_formatter(str(exp)))


async def main():
    # Create the logger and add the correlation_id to the logs.
    configure_tracing()
    logs_inject_correlation_id(logger)
    logger.info(
        "HL7 Listener started",
        logging_code='HL7LLOG001',
        settings=settings.dict(),
        messager_settings=messager_settings.dict()
    )

    #In case of cloud connect, the connect method will return empty handed
    await messager.connect()
    asyncio.create_task(hl7_receiver())
    await start_health_check_server()
    await asyncio.Event().wait()

    if messager.conn and hasattr(messager.conn, "close"):
        await messager.conn.close()


if __name__ == "__main__":
    asyncio.run(main())