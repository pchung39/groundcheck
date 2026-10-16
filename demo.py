rules = {
    "battery_voltage": {"min": 24.0, "max": 34.0},
    "battery_temp": {"min": 0.0, "max": 45.0},
}

samples = {
    "battery_voltage": [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
        {"timestamp": 101, "channel": "battery_voltage", "value": 23.5},
        {"timestamp": 102, "channel": "battery_voltage", "value": 28.0},
    ],
}
# channel summary
# eval results