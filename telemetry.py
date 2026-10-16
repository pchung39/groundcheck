import math

rules = {
    "battery_voltage": {"min": 24.0, "max": 34.0},
    "battery_temp": {"min": 0.0, "max": 45.0},
}

samples = [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
        {"timestamp": 100, "channel": "battery_temp", "value": 20.0},
        {"timestamp": 102, "channel": "battery_voltage", "value": 26.0},
        {"timestamp": 103, "channel": "battery_temp", "value": 24.0},
        {"timestamp": 101, "channel": "battery_voltage", "value": 30.0},
        {"timestamp": 101, "channel": "battery_temp", "value": 22.0},
    ]

'''
    {
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
'''

samples = {
    "battery_voltage": [
        {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
    ],
}

def validate_sample(sample):
    # you are checking a single record inside each sample

    # must be dict
    # must contain timestamp, channel, and value
    # timestamp but be an integer
    # channel must be a string with one or more characters
    # value must be an int or float

def find_violations(samples, rules):

    missing_channels = []
    violations = []

    print(samples)
    for sample_name, sample in samples.items():
        if sample_name not in rules:            
            next
        for item in sample:
            rule = rules[sample_name]
            value  = item["value"]

            if value < rule["min"] or value > rule["max"]:
                violations.append({
                    "channel": sample_name,
                    "timestamp": item["timestamp"],
                    "value": value,
                    "limit": "min" if value < rule["min"] else "max",
                    "threshold": rule["min"] if value < rule["min"] else rule["max"]
                })

    required_channels = set(rules)
    present_channels = {
        channel
        for channel, measurements in samples.items()
        if measurements
    }
    missing_channels = sorted(required_channels - present_channels)

    print(violations)
    return missing_channels, violations

def get_verdict(violations, missing_channels):

    if len(missing_channels) > 0 and len(violations) == 0:
        return "INSUFFICIENT_DATA"
    elif len(violations) > 0:
        return "NO-GO"
    else:
        return "GO" 

def evaluate_run(samples, rules):
    segmented = segment_channels(samples)
    missing_channels, violations = find_violations(segmented, rules)

    return {
        "verdict": get_verdict(violations, missing_channels),
        "violations": violations,
        "missing_channels": missing_channels
    }

def segment_channels(samples):

    h = {}

    for s in samples:
        channel_name = s['channel']
        if channel_name in h:
            h[channel_name].append(s)
        else:
            h[channel_name] = [s]

    return h

def summarize_channels(samples):
    
    result = {}

    segmented_channels = segment_channels(samples)

    for channel_name, channel_samples in segmented_channels.items():
        latest_sample = max(channel_samples, key=lambda s: s["timestamp"])

        result[channel_name] = {
            "count": len(channel_samples),
            "min": min(s["value"] for s in channel_samples),
            "max": max(s["value"] for s in channel_samples),
            "mean": sum(s["value"] for s in channel_samples) / len(channel_samples),
            "latest_value": latest_sample["value"],
            "latest_timestamp": latest_sample["timestamp"],
        }

    return result


