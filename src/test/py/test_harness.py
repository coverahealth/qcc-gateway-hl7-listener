"""Simple MLLP test harness for the HL7 listener.

Opens ONE connection and sends messages one after the other, waiting for each ACK:
--adts ADT messages, with --orus ORU messages spread evenly among them. Prints the time taken.

Usage:
    python src/test/py/test_harness.py --adts 300000 --orus 300
"""
import argparse
import asyncio
import time
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "resources" / "hl7_messages"
SB, EB = b"\x0b", b"\x1c\x0d"


def frame(name: str) -> bytes:
    text = (FIXTURES / name).read_text(encoding="utf-8", errors="ignore")
    return SB + text.replace("\r\n", "\r").replace("\n", "\r").encode() + EB


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2575)
    ap.add_argument("--adts", type=int, default=300_000, help="number of ADT messages")
    ap.add_argument("--orus", type=int, default=300, help="number of ORU messages sprinkled among the ADTs")
    a = ap.parse_args()

    adt, oru = frame("adt-a01-sample01.hl7"), frame("oru-r01-sample01.hl7")
    # Send an ORU after the ADT at each of these positions (evenly spaced).
    oru_positions = {(i + 1) * a.adts // (a.orus + 1) for i in range(a.orus)}

    reader, writer = await asyncio.open_connection(a.host, a.port)
    sent_adts = sent_orus = 0
    start = time.perf_counter()
    for i in range(1, a.adts + 1):
        writer.write(adt)
        await writer.drain()
        await reader.readuntil(EB)
        sent_adts += 1
        if i in oru_positions:
            writer.write(oru)
            await writer.drain()
            await reader.readuntil(EB)
            sent_orus += 1
    elapsed = time.perf_counter() - start
    writer.close()
    await writer.wait_closed()

    total = sent_adts + sent_orus
    print(f"Sent {sent_adts} ADTs + {sent_orus} ORUs = {total} messages, all ACKed")
    print(f"Time taken: {elapsed:.2f}s ({total / elapsed:.0f} msgs/s)")


if __name__ == "__main__":
    asyncio.run(main())
