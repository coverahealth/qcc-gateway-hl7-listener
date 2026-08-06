# Data Contracts & Schemas

## HL7 Message Format
Supports HL7 v2.4, v2.5, and v2.5.1 messages over MLLP protocol.

Standard HL7 segments processed:
- **MSH**: Message header (message type, timestamp, etc)
- **PID**: Patient identification
- **ORM/OBR**: Order information (studies, exams)
- **OBX**: Observation results

## HTTP Endpoint

### POST /hl7
Accepts raw HL7 messages via HTTP

**Request:**
```
Content-Type: text/plain
<VT>MSH|^~\&|SENDING_APP|SENDING_FAC|RECV_APP|RECV_FAC|...<CR><FS>
```

**Response (202 Accepted):**
```json
{
  "message_id": "msg-2026-08-06-001",
  "status": "queued",
  "processing_url": "/status/msg-2026-08-06-001"
}
```

## MLLP Protocol
- **Port**: 2575 (configurable)
- **Start Byte**: `0x0B` (VT - Vertical Tab)
- **End Bytes**: `0x1C 0x0D` (FS CR)

## Message Status

Processing states:
- `received` - Message received
- `parsing` - Extracting HL7 fields
- `validating` - Checking required fields
- `routing` - Determining target service
- `queued` - Awaiting downstream processing
- `processing` - Actively processing
- `completed` - Successfully processed
- `failed` - Processing error (will retry)
- `dead_lettered` - Permanently failed

## Error Responses

```json
{
  "error": "Invalid HL7 message",
  "error_code": "PARSE_ERROR",
  "details": "Missing required PID segment",
  "message_id": "msg-2026-08-06-001"
}
```
