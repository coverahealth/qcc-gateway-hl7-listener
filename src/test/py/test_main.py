"""Tests for main.py."""

import asyncio
import json
import os
from pathlib import Path
from unittest.mock import (
    AsyncMock,
    Mock
)
from hl7_listener.messaging.settings import CloudMessagingSettings
from covera_cloud_integration import CloudMessage
import pytest
import structlog
from covera import loglib
from nats.aio.client import Client as NATS_Client
from nats.aio.errors import ErrNoServers

from hl7_listener import main
from hl7_listener.messaging.nats import NATSMessager, PILOT_HEADER
from hl7_listener.settings import settings

package_directory = os.path.dirname(os.path.abspath(__file__))
root_path = "/../resources"
config_file = os.path.join(package_directory + root_path, "config.ini")
_hl7_messages_relative_dir = os.path.join(package_directory + root_path, "hl7_messages")



@pytest.fixture
def mock_pilot_settings(mocker) -> Mock:
    pilot_mode_mock = mocker.patch("hl7_listener.messaging.nats.msgr_config.settings")
    pilot_mode_mock.NATS_OUTGOING_SUBJECT = "test-subject"
    pilot_mode_mock.NATS_SERVER_URL = "test-url"
    pilot_mode_mock.PILOT_MODE.return_value = True
    return pilot_mode_mock


@pytest.mark.asyncio
async def test_nc_connect(monkeypatch):
    monkeypatch.setattr(NATS_Client, "connect", AsyncMock())
    result = await NATSMessager().connect()
    assert result is True

    monkeypatch.setattr(NATS_Client, "connect", AsyncMock(side_effect=ErrNoServers()))
    mock_ = NATSMessager()
    with pytest.raises(ErrNoServers):
        await mock_.connect()


@pytest.mark.asyncio
async def test_send_msg(mocker):
    mocker.patch.object(NATS_Client, "connect")
    mock_ = NATSMessager()
    await mock_.connect()
    my_asyncmock = AsyncMock()
    mocker.patch.object(mock_.conn, "request", new=my_asyncmock)
    await mock_.send_msg("test message")
    my_asyncmock.assert_awaited()


@pytest.mark.asyncio
async def test_send_msg_cloud_messaging(mocker):
    
    from hl7_listener.messaging.cloud_messaging import CloudMessager
    from hl7_listener.messaging import cloud_messaging
    cloud_messager = CloudMessager()
    mock_create_client = mocker.patch.object(cloud_messaging,"create_client")
    msgr_config_mock = mocker.patch.object(cloud_messaging,"msgr_config")
    msgr_config_mock.settings=CloudMessagingSettings()

    mock_client = AsyncMock()
    mock_create_client.return_value.__aenter__.return_value=mock_client
    mock_client.send_message=AsyncMock()
    await cloud_messager.send_msg("test message")
    mock_client.send_message.assert_called_once_with("test-queue",CloudMessage(data="test message",content_type="text/plain"),timeout=5)
    


@pytest.mark.asyncio
async def test_pilot(mock_pilot_settings, mocker):
    mocker.patch.object(NATS_Client, "connect")
    mock_ = NATSMessager()
    await mock_.connect()
    my_asyncmock = AsyncMock()
    mocker.patch.object(mock_.conn, "request", new=my_asyncmock)
    await mock_.send_msg("test message")
    my_asyncmock.assert_called_once_with(
        subject=mock_pilot_settings.NATS_OUTGOING_SUBJECT,
        payload="test message".encode(),
        timeout=10,
        headers=PILOT_HEADER
    )
    my_asyncmock.assert_awaited()


@pytest.mark.asyncio
async def test_processed_received_hl7_messages(mocker, caplog):
    with open(_hl7_messages_relative_dir + "/adt-a01-sample01.hl7", "r") as file:
        hl7_text = str(file.read())

    # Configure structlog using our package, use CapturingLoggerFactory to support
    # "log capture" for the test case
    clf = structlog.testing.CapturingLoggerFactory()
    loglib.configure(
        log_level="INFO",
        logging_processors=loglib.get_qcc_processors(),
        logger_factory=clf,
    )

    # Mock reader input parameter.
    asyncmock_reader = AsyncMock()
    asyncmock_reader.at_eof = Mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    mock_hl7_message = Mock()
    mocker.patch.object(mock_hl7_message, "__str__", return_value=hl7_text)
    mocker.patch.object(mock_hl7_message, "create_ack", return_value="ack")
    mocker.patch.object(asyncmock_reader, "readmessage", return_value=mock_hl7_message)

    # Mock writer input parameter.
    asyncmock_writer = AsyncMock()
    mocker.patch.object(
        asyncmock_writer, "get_extra_info", return_value="test_hl7_peername"
    )
    mocker.patch.object(asyncmock_writer, "writemessage")
    mocker.patch.object(asyncmock_writer, "drain")

    send_msg_mock = AsyncMock()
    mocker.patch.object(NATSMessager, "send_msg", new=send_msg_mock)

    # Above mocks setup to test the "happy" path.
    #
    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)
    # Expect default "Application Accept" (AA) ack_code.
    mock_hl7_message.create_ack.assert_called_once_with()
    asyncmock_writer.writemessage.assert_called_once_with("ack")
    asyncmock_writer.drain.assert_called_once()

    # Test force hl7 parse exception.
    # The exception should be handled and an Application Reject (AR) ack_code returned.
    #
    asyncmock_reader.reset_mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    asyncmock_writer.reset_mock()
    mock_hl7_message.reset_mock()
    # Last param needed to save mock calls.
    mocker.patch.object(mock_hl7_message, "create_ack", mock_hl7_message)
    mocker.patch.object(mock_hl7_message, "__str__", return_value="not an hl7 message")
    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)
    assert "ack_code='AR'" in str(mock_hl7_message.mock_calls[0])
    # Test asyncio.IncompleteReadError.
    # The exception is raised with this scenario.
    #
    asyncmock_reader.reset_mock()
    asyncmock_reader.at_eof.side_effect = [False, False]
    asyncmock_reader.readmessage.side_effect = RuntimeError("forced read failure")
    with pytest.raises(Exception, match="forced read failure"):
        await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)

    # Test general Exception after hl7_message is defined. This should result in
    # an Application Error (AE) ack_code and no raised exception.
    #
    asyncmock_reader.reset_mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    asyncmock_reader.readmessage.side_effect = None
    asyncmock_writer.reset_mock()
    mock_hl7_message.reset_mock()
    # Last param needed to save mock calls.
    mocker.patch.object(mock_hl7_message, "create_ack", mock_hl7_message)
    mocker.patch.object(mock_hl7_message, "__str__", return_value=hl7_text)
    send_msg_mock.side_effect = Exception("force exception from mock")
    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)

    assert "ack_code='AE'" in str(mock_hl7_message.mock_calls[0])

    # Verify a specific log statement has been spooled and has the proper context arguments
    found_log_statement = False
    for log_statement in [json.loads(log_call.args[0]) for log_call in clf.logger.calls]:
        if log_statement.get("message") == "HL7 Listener received a message":
            found_log_statement = True
            assert log_statement.get("logging_code") == "HL7LLOG003"
            assert log_statement.get("type") == "ADT^A01"
            break
    assert found_log_statement


@pytest.mark.parametrize(
    "file_name, expected_patient_name",
    [
        ("adt-a01-invalid-utf8.hl7", "EVERYMAN"),
        ("adt-a01-truncated-utf8.hl7", "EVERYMAN"),
    ],
)
@pytest.mark.asyncio
async def test_processed_received_hl7_messages_ignores_invalid_utf8(
    file_name,
    expected_patient_name,
    mocker,
):
    with open(_hl7_messages_relative_dir + f"/{file_name}", "rb") as file:
        hl7_text = file.read().decode("UTF-8", errors="ignore")

    assert expected_patient_name in hl7_text
    assert "\ufffd" not in hl7_text

    asyncmock_reader = AsyncMock()
    asyncmock_reader.at_eof = Mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    hl7_message = main.hl7.parse(hl7_text)
    mocker.patch.object(asyncmock_reader, "readmessage", return_value=hl7_message)

    asyncmock_writer = AsyncMock()
    mocker.patch.object(
        asyncmock_writer, "get_extra_info", return_value="test_hl7_peername"
    )
    mocker.patch.object(asyncmock_writer, "writemessage")
    mocker.patch.object(asyncmock_writer, "drain")

    send_msg_mock = mocker.patch.object(main.messager, "send_msg", new=AsyncMock())

    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)

    sent_message = send_msg_mock.await_args.kwargs["msg"]
    assert expected_patient_name in sent_message
    assert "\ufffd" not in sent_message
    asyncmock_writer.writemessage.assert_called_once()
    asyncmock_writer.drain.assert_called_once()


@pytest.mark.asyncio
async def test_processed_received_hl7_messages_removes_replacement_character(
    mocker,
):
    with open(
        _hl7_messages_relative_dir + "/adt-a01-valid-unicode-characters.hl7",
        "r",
        encoding="UTF-8",
    ) as file:
        hl7_text = file.read()

    assert "TE\ufffdST^José" in hl7_text

    asyncmock_reader = AsyncMock()
    asyncmock_reader.at_eof = Mock()
    asyncmock_reader.at_eof.side_effect = [False, True]
    hl7_message = main.hl7.parse(hl7_text)
    mocker.patch.object(asyncmock_reader, "readmessage", return_value=hl7_message)

    asyncmock_writer = AsyncMock()
    mocker.patch.object(
        asyncmock_writer, "get_extra_info", return_value="test_hl7_peername"
    )
    mocker.patch.object(asyncmock_writer, "writemessage")
    mocker.patch.object(asyncmock_writer, "drain")

    send_msg_mock = mocker.patch.object(main.messager, "send_msg", new=AsyncMock())

    await main.process_received_hl7_messages(asyncmock_reader, asyncmock_writer)

    sent_message = send_msg_mock.await_args.kwargs["msg"]
    assert "TEST^José" in sent_message
    assert "\ufffd" not in sent_message
    asyncmock_writer.writemessage.assert_called_once()
    asyncmock_writer.drain.assert_called_once()


@pytest.mark.asyncio
async def test_hl7_receiver_exception(mocker):
    # Session config parameters should result in a connection error that
    # raises an Exception.
    mocker.patch.object(
        main,
        "start_hl7_server",
        new=AsyncMock(side_effect=RuntimeError("forced receiver failure")),
    )

    with pytest.raises(Exception, match="forced receiver failure"):
        await main.hl7_receiver()


@pytest.mark.asyncio
async def test_hl7_receiver_ignores_invalid_encoding_bytes(mocker):
    mock_hl7_server = AsyncMock()
    mock_hl7_server.serve_forever.side_effect = asyncio.CancelledError()
    mock_start_hl7_server = mocker.patch.object(
        main,
        "start_hl7_server",
        new=AsyncMock(),
    )
    mock_start_hl7_server.return_value.__aenter__.return_value = mock_hl7_server

    await main.hl7_receiver()

    mock_start_hl7_server.assert_awaited_once_with(
        main.process_received_hl7_messages,
        host=settings.HL7_MLLP_HOST,
        port=int(settings.HL7_MLLP_PORT),
        encoding="UTF-8",
        encoding_errors="ignore",
    )
