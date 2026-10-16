from telemetry import summarize_channels, evaluate_run, validate_sample

def test_summarize_one_channel():
    samples = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
        {"timestamp": 102, "channel": "battery_voltage", "value": 26.0},
        {"timestamp": 101, "channel": "battery_voltage", "value": 30.0},
    ]

    result = summarize_channels(samples)

    assert result == {
        "battery_voltage": {
            "count": 3,
            "min": 26.0,
            "max": 30.0,
            "mean": 28.0,
            "latest_value": 26.0,
            "latest_timestamp": 102,
        }
    }

def test_summarize_multiple_channels():
    samples = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
        {"timestamp": 100, "channel": "battery_temp", "value": 20.0},
        {"timestamp": 102, "channel": "battery_voltage", "value": 26.0},
        {"timestamp": 103, "channel": "battery_temp", "value": 24.0},
        {"timestamp": 101, "channel": "battery_voltage", "value": 30.0},
        {"timestamp": 101, "channel": "battery_temp", "value": 22.0},
    ]

    result = summarize_channels(samples)

    assert result == {
        "battery_voltage": {
            "count": 3,
            "min": 26.0,
            "max": 30.0,
            "mean": 28.0,
            "latest_value": 26.0,
            "latest_timestamp": 102,
        },
        "battery_temp": {
            "count": 3,
            "min": 20.0,
            "max": 24.0,
            "mean": 22.0,
            "latest_value": 24.0,
            "latest_timestamp": 103,
        },
    }

def test_summarize_empty_input():
    assert summarize_channels([]) == {}

def test_evaluate_run_within_limits():
    rules = {
        "battery_voltage": {"min": 24.0, "max": 34.0},
    }
    samples = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
    ]

    assert evaluate_run(samples, rules) == {
        "verdict": "GO",
        "violations": [],
        "missing_channels": [],
    }


def test_evaluate_run_catches_earlier_low_value():
    rules = {
        "battery_voltage": {"min": 24.0, "max": 34.0},
    }
    samples = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 23.5},
        {"timestamp": 101, "channel": "battery_voltage", "value": 28.0},
    ]

    assert evaluate_run(samples, rules) == {
        "verdict": "NO-GO",
        "violations": [
            {
                "channel": "battery_voltage",
                "timestamp": 100,
                "value": 23.5,
                "limit": "min",
                "threshold": 24.0,
            }
        ],
        "missing_channels": [],
    }

def test_evaluate_run_missing_required_channel():
    rules = {
        "battery_voltage": {"min": 24.0, "max": 34.0},
        "battery_temp": {"min": 0.0, "max": 45.0},
    }

    samples = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
    ]

    assert evaluate_run(samples, rules) == {
        "verdict": "INSUFFICIENT_DATA",
        "violations": [],
        "missing_channels": ["battery_temp"],
    }

def test_evaluate_run_empty_samples():
    rules = {
        "battery_voltage": {"min": 24.0, "max": 34.0},
        "battery_temp": {"min": 0.0, "max": 45.0},
    }

    assert evaluate_run([], rules) == {
        "verdict": "INSUFFICIENT_DATA",
        "violations": [],
        "missing_channels": [
            "battery_temp",
            "battery_voltage",
        ],
    }

def test_evaluate_run_violation_and_missing_channel():
    rules = {
        "battery_voltage": {"min": 24.0, "max": 34.0},
        "battery_temp": {"min": 0.0, "max": 45.0},
    }

    samples = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 23.5},
    ]

    assert evaluate_run(samples, rules) == {
        "verdict": "NO-GO",
        "violations": [
            {
                "channel": "battery_voltage",
                "timestamp": 100,
                "value": 23.5,
                "limit": "min",
                "threshold": 24.0,
            }
        ],
        "missing_channels": ["battery_temp"],
    }