# Listener Capacity and ADT Drop (DEV-14194)

## ADT drop behaviour

| Setting | Default | Effect |
|---|---|---|
| `HL7_DROP_ADT_ENABLED` | `false` | When `true`, messages whose MSH-9.1 is `ADT` are not published to NATS / Service Bus. |

- Classification reuses the existing parse in `process_received_hl7_messages`; it looks only at the message type.
- Every message is ACKed (AA), dropped ADTs included. There is no ACK flag.
- ORUs and all other message types follow the normal path. With the flag off, behaviour is unchanged.
- Enable it only for the RANT gateway.

## How the listener handles load

- One asyncio event loop on one core. Extra connections do not add capacity.
- Per connection, messages are handled serially: read, process, ACK, drain. A sender that waits for each ACK is limited by round-trip time.
- Because the ACK is always sent, a sender is throttled by the listener and ADTs cannot build up a backlog that delays ORUs.
- No connection cap, read/idle timeout or custom stream limit (asyncio default 64 KiB).

## Measurements

The first table is from one developer laptop, listener running natively over loopback, NATS in Docker, `LOG_LEVEL=INFO` (one log line per message). These are not sizing guarantees.

Script: `src/test/scripts/mllp_load_test.py`. The 300K and 50K rows came from an earlier version of the script (ORU every 1,000 ADTs on one connection); the 10-connection row used several connections, which the current simple script no longer does.

| Scenario | ADT rate | ORU latency (median / p95 / max) |
|---|---|---|
| 300,000 ADTs, 1 connection, ORU after every 1,000 ADTs | 1,071 msgs/s (280 s) | 3.7 / 11.8 / 28.3 ms |
| 50,000 ADTs, 1 connection, ADTs only | 1,297 msgs/s | n/a |
| 50,000 ADTs, 1 connection, ORU after every 1,000 | 1,257 msgs/s | 3.5 / 12.1 / 37.3 ms |
| 100,000 ADTs, 10 connections, ORUs on a separate connection | ~1,640 msgs/s | 24.7 / 42.1 / 67.9 ms |

### Docker Compose (listener container, `local/docker-compose.yml`)

Listener built as an image and run with `HL7_DROP_ADT_ENABLED=true`, NATS alongside, harness on the host (Docker Desktop on macOS), `LOG_LEVEL=INFO`. Each harness connection sends one message at a time and waits for the ACK.

| | 1 node | 2 nodes |
|---|---|---|
| Load | 300,000 ADTs + 300 ORUs on 1 connection | 2 senders, one per node, each 150,000 ADTs + 150 ORUs |
| Wall time | 561.6 s (about 9.4 min) | 287.4 s (about 4.8 min) |
| Rate | 535 msgs/s | 1,046 msgs/s combined (531 and 525 msgs/s per node) |
| Container CPU (avg / peak) | 60% / 77% | 61% / 67% and 64% / 70% |
| Container memory | about 92 MiB | about 88 MiB each |
| Published to NATS | 300 (ORUs only) | 150 per node (ORUs only) |
| Errors | 0 | 0 |

- Throughput roughly doubled with a second node: each node kept the same per-node rate.
- Neither run saturated the container CPU. On one connection the limit is the per-message round trip, not listener CPU, which is why a second connection scales almost linearly.
- The two-node run simulates two senders. A single connection cannot be split across nodes without a load balancer, so RANT sending everything over one connection to one instance gets the single-node rate.
- Docker Desktop on macOS adds network overhead (single node: 535 msgs/s in Docker against 1,071 msgs/s native). `docker stats` sampling adds a little load. Prod runs on Linux behind Traefik, so treat these as relative numbers.

### Native run details

For the 300K run:
- 300 ORUs were published to NATS and no ADTs were.
- Listener CPU was about 82% of one core (about 230 s of CPU in 280 s).
- Listener memory was about 30 MB.

Expected load for RANT is about 300K/day, an average of about 3.5 msgs/s. A 2-hour batch of 300K is about 42 msgs/s, around 4% of the measured single-connection rate.

An in-process test, `test_adt_burst_does_not_disturb_oru_processing`, runs 5,000 ADTs with ORUs interleaved on one mocked connection and asserts only ORUs are published, all messages are ACKed, and no ORU stalls behind the ADTs.

## Production deployment notes

- `qcc-landscape-gateway-ansible` `docker-compose-qcc.yml.j2` sets no CPU or memory limit on `hl7-listener`.
- MLLP traffic goes through a Traefik TCP router (`mllp-router`, container port 8000). It was not part of these tests.
- `resources.yml` in `app-deployments` (128Mi memory, 100-500m CPU, 1 replica) applies to the Kubernetes deployment. A CPU-limited run was not done.

## Not measured / known gaps

- Single-connection rate with real network round-trip time per ACK.
- Throughput through Traefik, on Linux, and under a container CPU limit.
- Hardening gaps that exist today and are out of scope for this ticket: the 64 KiB stream limit, no read/idle timeout, and the `AR` error path that uses `hl7_message` when it may still be `None`.

## Running the load test

```bash
just start-prereq                      # NATS (also run: docker compose -f local/docker-compose.yml up nats-tools to create the stream)
HL7_MLLP_HOST=127.0.0.1 HL7_MLLP_PORT=2575 NATS_OUTGOING_SUBJECT=hl7.queue \
  NATS_SERVER_URL=127.0.0.1:4222 HL7_DROP_ADT_ENABLED=true poetry run python -m hl7_listener.main
python src/test/scripts/mllp_load_test.py --adts 300000 --orus 300
```

Run it against a listener on the host or in Docker Compose. The script opens one connection, sends the ADTs one after the other (waiting for each ACK) with the ORUs spread evenly among them, and prints the time taken. Options: `--host`, `--port`, `--adts`, `--orus`.

Without the JetStream stream, the first ORU publish fails and the listener closes the connection without an ACK.
