# qcc-gateway-hl7-listener
This is a Python service that receives and processes HL7 medical messages.

**Part of:** QCC Gateway ecosystem
**Purpose:** HL7 message reception and routing
**Language:** Python (async MLLP server)
**Port:** 2575 (MLLP), 8000 (HTTP)

## Quick Start

### Local Development
```bash
poetry install
direnv allow
just start-local   # Starts NATS and listener
just test          # Run tests
```

### Docker
```bash
just docker-build <user> <key>
just docker-up
```

---

## Overview
This service does the following:
* Listen/receive MLLP HL7 messages from the configured port.
* Publish (NATS Publish-Subscribe mode) the received HL7 messages to either the configured NATS JetStream server "Subject" (e.g., "hl7.<subject-name>") or configured Cloud Based queue.
Note that the "Subject" is associated with a JetStream "Stream" (e.g., "hl7") and the stream's "Consumer" (e.g.,"queue").
* The published NATS messages are acknowledge by the server. If messages publishes start to fail or acknowledges do not occur, listening for HL7 messages will halt.

Diagram: 
![Gateway Appliance](diagrams/gateway_appliance.png)

## Development

### Setup

```bash
poetry install # Create venv and install dependencies

poetry run pytest # Run unit tests

poetry build -f wheel # Build the wheel file under dist directory
```

## Env Vars
To run locally via docker you'll need to set a couple of env variables
```shell
export HL7_MLLP_HOST=<host>
export HL7_MLLP_PORT=<port>
export OUTBOUND_QUEUE_TYPE=<NATS or CLOUD>
#if cloud
export OUTBOUND_QUEUE_NAME=<queue name>
export MSG_NAMESPACE=<msg namespace>

#if hl7
export NATS_SERVER_URL=<server url>
```

Update `pyproject.toml` as needed.

```bash
poetry update # update the poetry.lock file after making changes to pyproject.toml
```

### Adding Dependencies

Update the `pyproject.toml` file to add dependencies.

### Install NATS Jetstream server and NATS CLI

You can find the instructions for the NATS Jetstream server (via docker) here:
https://hub.docker.com/_/nats/

You can find the instructions for the NATS Cli here:
https://github.com/nats-io/natscli

A `docker-compose` file is also available for standing up NATS Jetstream server.

### Create the stream and consumer

Create the hl7 stream with wildcard/unspecified subjects:

```bash
nats str add hl7 --subjects "hl7.*" --ack --max-msgs=-1 --max-bytes=-1 --max-age=1y --storage file --retention limits --max-msg-size=-1 --discard=old --max-msgs-per-subject=-1 --dupe-window=2m --replicas=1
```

Create the queue consumer for the hl7 stream and filter to a subject named "hl7.queue":

```bash
nats con add hl7 queue --filter hl7.queue --ack explicit --pull --deliver all --max-deliver=-1 --sample 100 --max-pending=1 --replay=instant --wait=1s
```
### Environment variables

You will need to override these if you are not running locally.

HL7_MLLP_HOST = HL7 MLLP host server

HL7_MLLP_PORT = HL7 MLLP host server port to listen for incoming HL7 messages

PILOT_MODE = Flag that delineate whether to skip membership check

NATS_OUTGOING_SUBJECT = NATS subject to use

NATS_SERVER_URL = NATS Jetstream connection info

OUTBOUND_QUEUE_TYPE = one of: NATS, CLOUD

OUTBOUND_QUEUE_NAME = Name of queue to send to

### Creating the docker image

Create the container using the docker build command below.

```bash
docker build -t qcc-gateway-hl7-listener:1.0.0 .
```

If the steps completed successfully, the image specified by the -t option should now exist.

## Testing

### With NATS Config

Install nats cli
```bash
brew tap nats-io/nats-tools
brew install nats-io/nats-tools/nats
```

Set local context
```bash
nats context add local --description "Localhost"
nats context ls
nats context select local
```

Make sure your NATS-specific environment vars are set. They are:
- NATS_OUTGOING_SUBJECT
- NATS_SERVER_URL
- OUTBOUND_QUEUE_TYPE

Start the services
```bash
docker-compose up
```

Create a stream (hl7) and a consumer (hl7.queue) for that stream
```bash
nats str add hl7 --subjects "hl7.*" --ack --max-msgs=-1 --max-bytes=-1 --max-age=1y --storage file --retention limits --max-msg-size=-1 --discard=old --max-msgs-per-subject=-1 --dupe-window=2m --replicas=1

nats con add hl7 queue --filter hl7.queue --ack explicit --pull --deliver all --max-deliver=-1 --sample 100 --max-pending=1 --replay=instant --wait=1s
```

Send a sample HL7 using `HL7 Inspector` tool. Samples are available under `src/test/resources`. Import a sample file in Hl7 inspector. Set the send option to the following:

![send options](diagrams/hl7_inspector_send_option.png)

Hit the send button and confirm success in the logs: 
![send confirmation](diagrams/hl7_inspector_send_confirmation.png)

Confirm the message was processed by the service and sent to hl7.queue consumer ("Unprocessed Messages": 1)
```bash
nats con info hl7 queue
```

### With Queue Config

Make sure your Cloud-specific environment vars are set. They are:
- OUTBOUND_QUEUE_NAME
- OUTBOUND_QUEUE_TYPE

Start the services
```bash
docker-compose up
```

Send a sample HL7 using `HL7 Inspector` tool. Samples are available under `src/test/resources`. Import a sample file in Hl7 inspector. Set the send option to the following:

![send options](diagrams/hl7_inspector_send_option.png)

Hit the send button and confirm success in the logs:
![send confirmation](diagrams/hl7_inspector_send_confirmation.png)

Confirm the message was processed by the service and sent to Cloud queue your environment points to.

## Network & Ports

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| MLLP Listener | 2575 | TCP | HL7 message reception |
| HTTP API | 8000 | HTTP | Status and management |
| NATS | 4222 | TCP | Message queue |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused on port 2575 | Service not listening | Start service: `just start-local` |
| HL7 messages not processed | NATS not running | Start NATS: `docker-compose up nats` |
| ACK not sent to sender | Outgoing queue blocked | Check NATS `hl7.queue` consumer status |
| Port 2575 already in use | Another service running | Kill process: `lsof -i :2575` |
| Parse error on valid HL7 | Validation too strict | Set `VALIDATION_STRICT=false` |
| Messages in dead letter queue | Permanent parsing failures | Check sample in `tests/fixtures/` for comparison |

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Project context and configuration
- **[docs/design.md](docs/design.md)** - Service architecture
- **[docs/data-contracts.md](docs/data-contracts.md)** - HL7 message schemas
- **[docs/testing.md](docs/testing.md)** - Testing guide
- **[QCC Project Overview](../../qcc_project_overview.md)**

## Graphify Knowledge Graph

Initialize (one-time):
```bash
graphify claude install
graphify hook install
graphify update .
graphify query "what HL7 segments are parsed"
```