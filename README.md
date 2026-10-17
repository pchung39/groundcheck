```
         ___
      __/   \__
     /    ▲    \
    |  GROUND   |
    |   CHECK   |
     \_________/
      preflight
```

## What GroundCheck does

GroundCheck reads a telemetry run and decides if it is safe to proceed. It checks each sample against per-channel min and max limits, reports every out-of-range reading, and flags required channels that never showed up.

## How to run the demo

```bash
source .venv/bin/activate
python demo.py
```

## How to run the tests

```bash
source .venv/bin/activate
pytest
```

## Input format

`evaluate_run(samples, rules)` takes a flat list of samples:

```python
samples = [
    {"timestamp": 100, "channel": "battery_voltage", "value": 28.0},
]

rules = {
    "battery_voltage": {"min": 24.0, "max": 34.0},
}
```

`timestamp` is an int. `channel` is a non-empty string. `value` is an int or float. Each rule is a channel name with a `min` and a `max`.

## Verdict rules

| Verdict | When |
| --- | --- |
| `GO` | Every required channel has data, and every value is inside its limits. |
| `NO-GO` | At least one value is below `min` or above `max`. This wins even if a required channel is also missing. |
| `INSUFFICIENT_DATA` | A required channel has no samples, and nothing is out of range. |

A violation record includes the channel, timestamp, value, which limit failed (`"min"` or `"max"`), and the threshold.

## Current limitations

- `demo.py` only defines example data. It does not print a summary or a verdict yet.
- `validate_sample` is not implemented.
- A channel that appears in the samples but not in the rules is not handled cleanly.
- Limits are a single min/max pair. There is no rate-of-change check, no units, and no time alignment across channels.
