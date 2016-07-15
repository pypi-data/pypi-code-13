
class Errors(object):
    TRACE_COUNT_OFF = "trace_count_off"

def check_trace(trace, errors):
    entries = trace.counter
    labels = 0
    bridge_count = 0
    for _, counter in trace.point_counters.items():
        labels += counter
    for bridge in trace.bridges:
        bridge_count += bridge.counter
    if entries < labels:
        errors.report(Errors.TRACE_COUNT_OFF,
            "trace entered %d times, %d ")
