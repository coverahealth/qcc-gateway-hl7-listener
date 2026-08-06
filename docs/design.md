# Architecture & Design

## Overview
HL7 Listener service processes incoming HL7 medical messages and routes them to appropriate downstream services for processing.

## Service Purpose
- Receive HL7 messages from external systems
- Parse and validate HL7 message structure
- Extract patient and study metadata
- Route messages to appropriate processors
- Track message processing status

## Core Components

### Message Receivers
- MLLP (Minimal Lower Layer Protocol) for hospital integration
- HTTP endpoints for cloud sources
- SFTP for file-based transfers

### Processing Pipeline
1. **Message Parsing**: Validate and parse HL7 syntax
2. **Validation**: Check required fields and structure
3. **Enrichment**: Add metadata and context
4. **Routing**: Determine target service
5. **Delivery**: Queue for processing

### External Dependencies
- Hospital systems (HL7 senders)
- Downstream services (processors)
- Message queue (NATS or similar)
- Patient database (optional lookup)

## Design Patterns
- **Protocol Adapters**: MLLP, HTTP, SFTP support
- **Async Processing**: Non-blocking message handling
- **Dead Letter Queues**: Handle malformed messages
- **Circuit Breaker**: Downstream service failures

## Configuration
- MLLP port (typically 2575)
- HTTP endpoints
- SFTP credentials
- Message routing rules
- Retry policies
