# Testing Guide

## Test Structure
```
tests/
├── unit/           # HL7 parsing, validation
├── integration/    # With mock MLLP clients
└── fixtures/       # Sample HL7 messages
```

## Running Tests
```bash
just test
poetry run pytest tests/ -v
poetry run pytest --cov=src --cov-report=html
```

## Test Data
Sample HL7 messages in `tests/fixtures/`:
- `sample_orm_msg.hl7` - Order message
- `sample_adt_msg.hl7` - Patient admission
- `invalid_msg.hl7` - Malformed message

## MLLP Testing
```python
import socket
msg = b'\x0bMSH|...\x1c\x0d'  # Wrapped in MLLP
socket.send(msg)
```

## Datadog Integration
HL7 message receive events are traced in Datadog for monitoring message flow.

## Debugging
```bash
LOG_LEVEL=DEBUG just start-local
# Enable MLLP protocol tracing
export MLLP_DEBUG=1
```
