ERROR_KEYWORDS = [
    "timeout",
    "failed",
    "exception",
    "critical",
    "denied",
    "unauthorized"
]


def correlate_incidents(parsed_logs):

    correlated_logs = []

    for log in parsed_logs:

        message = log.get(
            "message",
            ""
        ).lower()

        for keyword in ERROR_KEYWORDS:

            if keyword in message:

                correlated_logs.append(log)

                break

    return correlated_logs