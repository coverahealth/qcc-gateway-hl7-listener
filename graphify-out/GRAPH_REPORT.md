# Graph Report - qcc-gateway-hl7-listener  (2026-10-28)

## Corpus Check
- 20 files · ~20,613 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 269 nodes · 313 edges · 23 communities (20 shown, 3 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `24ef7691`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]

## God Nodes (most connected - your core abstractions)
1. `NATSMessager` - 11 edges
2. `qcc-gateway-hl7-listener Project Context` - 11 edges
3. `qcc-gateway-hl7-listener Project Context` - 11 edges
4. `qcc-gateway-hl7-listener` - 10 edges
5. `qcc-gateway-hl7-listener` - 10 edges
6. `Env Vars` - 8 edges
7. `DEV-14194: RANT Gateway – accept and immediately drop high-volume ADTs` - 8 edges
8. `Testing Guide` - 8 edges
9. `_process_hl7_texts()` - 7 edges
10. `hl7_receiver()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `test_send_msg_cloud_messaging()` --calls--> `CloudMessager`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/cloud_messaging.py
- `NATSMessager` --uses--> `MessagingInterface`  [INFERRED]
  src/main/py/hl7_listener/messaging/nats.py → src/main/py/hl7_listener/messaging/base.py
- `test_nc_connect()` --calls--> `NATSMessager`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/nats.py
- `test_send_msg()` --calls--> `NATSMessager`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/nats.py
- `test_send_msg_cloud_messaging()` --calls--> `CloudMessagingSettings`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/settings.py

## Communities (23 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (20): Architecture, Code Structure, Commands, Configuration, Data Contracts, Development, Environment Variables, Graphify (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (20): Adding Dependencies, Create the stream and consumer, Creating the docker image, Development, Docker, Env Vars, Environment variables, Graphify Knowledge Graph (+12 more)

### Community 2 - "Community 2"
Cohesion: 0.20
Nodes (7): BaseSettings, Enum, QueueType, Settings, CloudMessagingSettings, NATSSettings, test_send_msg_cloud_messaging()

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (35): NATSMessager, Connect to the NATS jetstream server., Connect to the NATS jetstream server., Synchronously (no callback or async ACK) send the input message to the NATS, Synchronously (no callback or async ACK) send the input message to the NATS, adt_text(), mock_pilot_settings(), oru_text() (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (7): ABC, Any, MessagingInterface, CloudMessager, Dont need this method so basically just putting a pass on it since we create cli, Sends a msg to an cloud messaging queue., MessagingInterface

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (11): code:block1 (tests/), code:bash (just test), code:python (import socket), code:bash (LOG_LEVEL=DEBUG just start-local), Datadog Integration, Debugging, MLLP Testing, Running Tests (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.23
Nodes (11): health_check_handler(), start_health_check_server(), exception_formatter(), hl7_receiver(), main(), process_received_hl7_messages(), This HL7 MLLP Listener/Receiver Service will do the following:  1) Connect to th, Receive HL7 MLLP messages on the configured host and port. (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (9): Architecture & Design, Configuration, Core Components, Design Patterns, External Dependencies, Message Receivers, Overview, Processing Pipeline (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (10): code:block1 (Content-Type: text/plain), code:json ({), code:json ({), Data Contracts & Schemas, Error Responses, HL7 Message Format, HTTP Endpoint, Message Status (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (25): Architecture, Code Structure, code:bash (brew bundle), code:bash (graphify claude install), code:block3 (src/), code:bash (just test                              # All tests), code:bash (graphify install), Commands (+17 more)

### Community 14 - "Community 14"
Cohesion: 0.08
Nodes (24): code:bash (poetry install), code:bash (nats context add local --description "Localhost"), code:bash (docker-compose up), code:bash (nats str add hl7 --subjects "hl7.*" --ack --max-msgs=-1 --ma), code:bash (nats con info hl7 queue), code:bash (docker-compose up), code:bash (graphify claude install), code:bash (just docker-build <user> <key>) (+16 more)

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (10): ADT drop behaviour, code:bash (just start-prereq                      # NATS (also run: doc), Docker Compose (listener container, `local/docker-compose.yml`), How the listener handles load, Listener Capacity and ADT Drop (DEV-14194), Measurements, Native run details, Not measured / known gaps (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (11): Adding Dependencies, code:shell (export HL7_MLLP_HOST=<host>), code:bash (poetry update # update the poetry.lock file after making cha), code:bash (nats str add hl7 --subjects "hl7.*" --ack --max-msgs=-1 --ma), code:bash (nats con add hl7 queue --filter hl7.queue --ack explicit --p), code:bash (docker build -t qcc-gateway-hl7-listener:1.0.0 .), Create the stream and consumer, Creating the docker image (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.22
Nodes (8): Code changes (`src/main/py/hl7_listener/`), Context, Deploy/config (sibling repos, separate PRs), DEV-14194: RANT Gateway – accept and immediately drop high-volume ADTs, Docs, Open risks, Tests, Verification

### Community 18 - "Community 18"
Cohesion: 0.67
Nodes (3): frame(), main(), Simple MLLP test harness for the HL7 listener.  Opens ONE connection and sends m

## Knowledge Gaps
- **102 isolated node(s):** `PreToolUse`, `code:bash (poetry install)`, `code:bash (just docker-build <user> <key>)`, `Overview`, `code:bash (poetry install # Create venv and install dependencies)` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `NATSMessager` connect `Community 3` to `Community 4`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `qcc-gateway-hl7-listener Project Context` connect `Community 0` to `Community 7`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `qcc-gateway-hl7-listener` connect `Community 1` to `Community 7`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `NATSMessager` (e.g. with `MessagingInterface` and `test_nc_connect()`) actually correct?**
  _`NATSMessager` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PreToolUse`, `Non-pilot case: the per-message correlation_id must reach the NATS headers.`, `When no correlation context is installed, the header must be omitted (not     No` to the rest of the system?**
  _120 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._