from packet import decode_measurement
from telemetry import summarize_channels, evaluate_run

def process_packets(packets, rules):
    samples = []
    for packet in packets:
        decoded = decode_measurement(packet)
        samples.append(decoded)
    
    return {
        "summaries": summarize_channels(samples),
        "evaluation": evaluate_run(samples, rules),
    }
    