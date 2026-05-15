def reconstruct_timeline(parsed_logs):

    sorted_logs = sorted(
        parsed_logs,
        key=lambda x: x.get("timestamp", "")
    )

    timeline = []

    for log in sorted_logs:

        timeline.append({
            "timestamp": log.get("timestamp"),
            "service": log.get("service"),
            "message": log.get("message"),
            "level": log.get("level")
        })

    return timeline