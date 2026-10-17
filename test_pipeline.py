from packet import encode_measurement
from pipeline import process_packets


def test_packets_to_summaries_and_verdict():
    rules = {
        "battery_voltage": {"min": 24.0, "max": 34.0},
        "battery_temp": {"min": 0.0, "max": 45.0},
    }

    measurements = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
        {"timestamp": 101, "channel": "battery_voltage", "value": 23.5},
        {"timestamp": 102, "channel": "battery_voltage", "value": 28.0},
        {"timestamp": 100, "channel": "battery_temp", "value": 22.0},
    ]

    packets = [
        encode_measurement(measurement)
        for measurement in measurements
    ]

    result = process_packets(packets, rules)
    voltage_summary = result["summaries"]["battery_voltage"]

    assert voltage_summary["count"] == 3
    assert voltage_summary["min"] == 23.5
    assert voltage_summary["max"] == 28.0
    assert voltage_summary["latest_value"] == 28.0
    assert voltage_summary["latest_timestamp"] == 102

    assert result["evaluation"] == {
        "verdict": "NO-GO",
        "violations": [
            {
                "channel": "battery_voltage",
                "timestamp": 101,
                "value": 23.5,
                "limit": "min",
                "threshold": 24.0,
            }
        ],
        "missing_channels": [],
    }