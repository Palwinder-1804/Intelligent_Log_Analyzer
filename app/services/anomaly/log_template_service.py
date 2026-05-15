import re


IP_PATTERN = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

NUMBER_PATTERN = r"\d+"


def normalize_log(log: str):

    log = re.sub(
        IP_PATTERN,
        "<IP>",
        log
    )

    log = re.sub(
        NUMBER_PATTERN,
        "<NUM>",
        log
    )

    return log.strip().lower()