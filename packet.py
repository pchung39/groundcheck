import struct
from telemetry import validate_sample

CHANNEL_IDS = {
    "battery_voltage": 100,
    "battery_temp": 101,
}

FORMAT_STRING = ">IHd"

def encode_measurement(measurement):
    validate_sample(measurement)
    if measurement['timestamp'] < 0 or measurement["timestamp"] > 4_294_967_295:
        raise ValueError("Timestamp out of bounds")
    
    if measurement["channel"] not in CHANNEL_IDS.keys():
        raise ValueError("Cannot find channel name in CHANNEL_IDS")

    # timestamp
    timestamp = measurement["timestamp"]
    channel_id = CHANNEL_IDS[measurement["channel"]]
    value = measurement["value"]

    return struct.pack(FORMAT_STRING, timestamp, channel_id, value)


def decode_measurement(packet):
    if not isinstance(packet, bytes):
        raise ValueError("packet must be bytes")

    if len(packet) != 14:
        raise ValueError("packet must be exactly 14 bytes")

    decoded = struct.unpack(FORMAT_STRING, packet)

    channel = next((k for k, v in CHANNEL_IDS.items() if v == decoded[1]), None)
    if channel is None:
        raise ValueError("Cannot find channel name in CHANNEL_IDS")

    measurement = {
        "timestamp": decoded[0],
        "channel": channel,
        "value": decoded[2]
    }

    validate_sample(measurement)

    return measurement
