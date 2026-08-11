# qcc-gateway-hl7-listener Project Context

## Project Overview
**HL7 Listener** - Receives and processes HL7 medical messages from external healthcare systems.

### Purpose
- Accept HL7 messages from hospital systems and external sources
- Parse and validate HL7 message structure
- Extract patient and study metadata
- Route messages to appropriate downstream services
- Provide acknowledgments to sending systems

### Key Responsibilities
- **MLLP Server**: Listen for incoming HL7 messages via MLLP protocol
- **Message Parsing**: Extract HL7 segments and fields
- **NATS Publishing**: Route messages to NATS JetStream
- **Error Handling**: Halt on NATS failures to prevent message loss
- **Health Monitoring**: Provide health check endpoint for orchestration

### Technology Stack
- **Language**: Python 3.9+
- **Protocol**: MLLP (Minimal Lower Layer Protocol)
- **HL7 Library**: python-hl7
- **Message Queue**: NATS JetStream
- **Async**: asyncio for concurrent connections
- **Health Check**: HTTP server for K8s probes

## Commands

### Development
```bash
brew bundle
poetry install
direnv allow
just start-local
just test
just docker-build <user> <key>
```

### Graphify
```bash
graphify claude install
graphify hook install
graphify update .
graphify query "show me all HL7 segments handled"
```

## Architecture

### Service Boundaries
- **Upstream**: Hospital systems, imaging centers, cloud sources
- **Downstream**: Processing services (packager, report uploader, etc)
- **Message Queue**: NATS for async routing

### Key Design Patterns
1. **Protocol Adapters**: MLLP, HTTP, SFTP receivers
2. **Async Processing**: Non-blocking message parsing
3. **ACK Management**: HL7 acknowledgments for reception
4. **Dead Letter Queue**: Failed messages for investigation
5. **Field Mapping**: Map HL7 to internal data models

## Code Structure
```
src/
├── main.py
├── config.py
├── models/
│   ├── hl7_message.py
│   ├── patient.py
│   └── order.py
├── services/
│   ├── mllp_listener.py
│   ├── hl7_parser.py
│   ├── message_router.py
│   └── hl7_acknowledger.py
├── api/
│   └── routes.py
└── utils/
    ├── hl7_utils.py
    └── protocol.py

tests/
├── unit/
├── integration/
└── fixtures/
```

## Configuration

### Environment Variables
**MLLP Server:**
- `MLLP_HOST`: Bind address (0.0.0.0)
- `MLLP_PORT`: Listen port (2575)
- `MLLP_TIMEOUT`: Connection timeout (seconds)

**HTTP Endpoints:**
- `HTTP_PORT`: HTTP API port (8000)

**Message Processing:**
- `MESSAGE_ROUTING_RULES`: JSON file mapping message types to targets
- `VALIDATION_STRICT`: Strict/lenient HL7 validation (true/false)
- `MAX_MESSAGE_SIZE_MB`: Maximum HL7 message size

**Queue:**
- `NATS_SERVERS`: NATS server addresses
- `NATS_OUTGOING_SUBJECT`: Routing topic (e.g., `hl7.processed`)

**Datadog:**
- `DD_TRACE_ENABLED`: Enable APM
- `DD_ENV`: Environment (dev, staging, prod)

## Data Contracts

See `docs/data-contracts.md` for HL7 schemas.

### Key Endpoints
- `POST /hl7` - Receive HL7 message via HTTP
- `GET /status/{msg_id}` - Check processing status
- `GET/health` - Service health

## Testing

See `docs/testing.md` for comprehensive testing guide.

```bash
just test                              # All tests
poetry run pytest tests/unit/ -v       # Unit only
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection timeout on MLLP port | Service not listening | Check `MLLP_PORT`, ensure service running |
| HL7 parse error | Malformed message | Check HL7 structure in test fixtures |
| Messages not routing | Routing rules misconfigured | Verify `MESSAGE_ROUTING_RULES` config |
| ACK not sent | Outgoing queue full | Check NATS connectivity |
| Max retries exceeded | Downstream service down | Verify target service health |
| Port already in use | Another service on 2575 | Change `MLLP_PORT` or kill other process |

## Related Documentation
- [docs/design.md](docs/design.md) - Architecture
- [docs/data-contracts.md](docs/data-contracts.md) - HL7 schemas
- [docs/testing.md](docs/testing.md) - Testing guide
- [README.md](README.md) - Getting started
- [QCC Project Overview](../../qcc_project_overview.md)

## Graphify Integration
```bash
graphify install
graphify update .
graphify query "what HL7 segments are processed"
```
