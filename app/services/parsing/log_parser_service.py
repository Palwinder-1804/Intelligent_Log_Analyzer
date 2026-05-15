import re


LOG_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) ([\w\-]+) (.*)"


def parse_log_line(log_line: str):

    match = re.match(LOG_PATTERN, log_line)

    if not match:
        return {
            "raw_log": log_line.strip(),
            "parsed": False
        }

    timestamp, level, service, message = match.groups()

    ip_match = re.search(
        r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
        message
    )

    ip_address = ip_match.group(0) if ip_match else None

    return {
        "timestamp": timestamp,
        "level": level,
        "service": service,
        "message": message,
        "ip_address": ip_address,
        "parsed": True
    }