# Graph Report - qcc-gateway-hl7-listener  (2026-08-06)

## Corpus Check
- 17 files · ~17,679 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 122 nodes · 131 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7ad45e38`
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

## God Nodes (most connected - your core abstractions)
1. `qcc-gateway-hl7-listener Project Context` - 11 edges
2. `qcc-gateway-hl7-listener` - 10 edges
3. `NATSMessager` - 7 edges
4. `Testing Guide` - 7 edges
5. `MessagingInterface` - 6 edges
6. `Env Vars` - 6 edges
7. `Data Contracts & Schemas` - 6 edges
8. `Architecture & Design` - 6 edges
9. `CloudMessager` - 5 edges
10. `hl7_receiver()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `NATSMessager` --uses--> `MessagingInterface`  [INFERRED]
  src/main/py/hl7_listener/messaging/nats.py → src/main/py/hl7_listener/messaging/base.py
- `test_send_msg_cloud_messaging()` --calls--> `CloudMessager`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/cloud_messaging.py
- `test_nc_connect()` --calls--> `NATSMessager`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/nats.py
- `test_pilot()` --calls--> `NATSMessager`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/nats.py
- `test_send_msg()` --calls--> `NATSMessager`  [INFERRED]
  src/test/py/test_main.py → src/main/py/hl7_listener/messaging/nats.py

## Import Cycles
- None detected.

## Communities (14 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (20): Architecture, Code Structure, Commands, Configuration, Data Contracts, Development, Environment Variables, Graphify (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (14): Development, Docker, Graphify Knowledge Graph, Local Development, Network & Ports, Overview, qcc-gateway-hl7-listener, Quick Start (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.19
Nodes (8): BaseSettings, Enum, QueueType, Settings, CloudMessagingSettings, NATSSettings, test_send_msg_cloud_messaging(), str

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (6): NATSMessager, Connect to the NATS jetstream server., Synchronously (no callback or async ACK) send the input message to the NATS, test_nc_connect(), test_pilot(), test_send_msg()

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (6): ABC, Any, MessagingInterface, CloudMessager, Dont need this method so basically just putting a pass on it since we create cli, Sends a msg to an cloud messaging queue.

### Community 5 - "Community 5"
Cohesion: 0.21
Nodes (7): Datadog Integration, Debugging, MLLP Testing, Running Tests, Test Data, Test Structure, Testing Guide

### Community 6 - "Community 6"
Cohesion: 0.25
Nodes (8): start_health_check_server(), exception_formatter(), hl7_receiver(), main(), process_received_hl7_messages(), This HL7 MLLP Listener/Receiver Service will do the following:  1) Connect to th, Receive HL7 MLLP messages on the configured host and port., This will be called every time a socket connects to the receiver/listener.

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (9): Architecture & Design, Configuration, Core Components, Design Patterns, External Dependencies, Message Receivers, Overview, Processing Pipeline (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.29
Nodes (7): Data Contracts & Schemas, Error Responses, HL7 Message Format, HTTP Endpoint, Message Status, MLLP Protocol, POST /hl7

### Community 9 - "Community 9"
Cohesion: 0.33
Nodes (6): Adding Dependencies, Create the stream and consumer, Creating the docker image, Env Vars, Environment variables, Install NATS Jetstream server and NATS CLI

## Knowledge Gaps
- **50 isolated node(s):** `nats.sh script`, `qcc-gateway-hl7-listener`, `Any`, `Purpose`, `Key Responsibilities` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `qcc-gateway-hl7-listener Project Context` connect `Community 0` to `Community 5`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `qcc-gateway-hl7-listener` connect `Community 1` to `Community 9`, `Community 5`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Why does `Architecture & Design` connect `Community 7` to `Community 5`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `NATSMessager` (e.g. with `MessagingInterface` and `test_nc_connect()`) actually correct?**
  _`NATSMessager` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `MessagingInterface` (e.g. with `CloudMessager` and `NATSMessager`) actually correct?**
  _`MessagingInterface` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `nats.sh script`, `qcc-gateway-hl7-listener`, `This HL7 MLLP Listener/Receiver Service will do the following:  1) Connect to th` to the rest of the system?**
  _57 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._