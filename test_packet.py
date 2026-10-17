import pytest
import struct
from packet import encode_measurement, decode_measurement


def test_encoded_packet_is_14_bytes():
    measurement = {
        "timestamp": 100,
        "channel": "battery_voltage",
        "value": 28.0,
    }

    packet = encode_measurement(measurement)

    assert isinstance(packet, bytes)
    assert len(packet) == 14


def test_voltage_round_trip():
    measurement = {
        "timestamp": 100,
        "channel": "battery_voltage",
        "value": 28.1,
    }

    packet = encode_measurement(measurement)
    decoded = decode_measurement(packet)

    assert decoded["timestamp"] == measurement["timestamp"]
    assert decoded["channel"] == measurement["channel"]
    assert decoded["value"] == pytest.approx(measurement["value"])

def test_temperature_round_trip():
    measurement = {
        "timestamp": 102,
        "channel": "battery_temp",
        "value": -5.5,
    }

    packet = encode_measurement(measurement)
    decoded = decode_measurement(packet)

    assert decoded["timestamp"] == measurement["timestamp"]
    assert decoded["channel"] == measurement["channel"]
    assert decoded["value"] == pytest.approx(measurement["value"])

def test_encode_rejects_unknown_channel():
    measurement = {
        "timestamp": 100,
        "channel": "unknown_sensor",
        "value": 28.0,
    }

    with pytest.raises(ValueError):
        encode_measurement(measurement)


@pytest.mark.parametrize("timestamp", [-1, 4_294_967_296])
def test_encode_rejects_out_of_range_timestamp(timestamp):
    measurement = {
        "timestamp": timestamp,
        "channel": "battery_voltage",
        "value": 28.0,
    }

    with pytest.raises(ValueError):
        encode_measurement(measurement)

def test_decode_rejects_non_bytes():
    with pytest.raises(ValueError):
        decode_measurement("not a packet")


@pytest.mark.parametrize("length", [0, 13, 15])
def test_decode_rejects_wrong_length(length):
    packet = b"\x00" * length

    with pytest.raises(ValueError):
        decode_measurement(packet)


def test_decode_rejects_unknown_channel_id():
    packet = struct.pack(">IHd", 100, 999, 28.0)

    with pytest.raises(ValueError):
        decode_measurement(packet)


@pytest.mark.parametrize(
    "value",
    [float("nan"), float("inf"), float("-inf")],
)
def test_decode_rejects_nonfinite_value(value):
    packet = struct.pack(">IHd", 100, 100, value)

    with pytest.raises(ValueError):
        decode_measurement(packet)