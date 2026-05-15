import pandas as pd


def _parse_event_list(raw_value: str) -> list[str]:
    trace_str = str(raw_value).strip()

    if trace_str.startswith("[") and trace_str.endswith("]"):
        trace_str = trace_str[1:-1]

    if "," in trace_str:
        events = [event.strip() for event in trace_str.split(",") if event.strip()]
    else:
        events = trace_str.split()

    return events


def load_event_traces(csv_path: str) -> list[list[str]]:
    df = pd.read_csv(csv_path)

    if "Features" in df.columns:
        trace_column = df["Features"]
    else:
        trace_column = df.iloc[:, 0]

    traces = []

    for raw_trace in trace_column:
        if pd.isna(raw_trace):
            continue

        events = _parse_event_list(raw_trace)

        if not events:
            continue

        traces.append(events)

    return traces
