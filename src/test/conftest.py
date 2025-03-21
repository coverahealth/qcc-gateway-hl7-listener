import os

os.environ["HL7_MLLP_HOST"] = "hl7-mllp-host"
os.environ["HL7_MLLP_PORT"] = "4444"
os.environ["NATS_SERVER_URL"] = "nats-server"
os.environ["OUTBOUND_QUEUE_TYPE"] = "NATS"
os.environ["OUTBOUND_QUEUE_NAME"] = "test-queue"
os.environ["MSG_NAMESPACE"] ="message_ns"