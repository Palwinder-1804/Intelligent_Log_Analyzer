import pandas as pd


LEVEL_MAPPING = {
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
    "CRITICAL": 4
}


def extract_features(parsed_logs):

    features = []

    for log in parsed_logs:

        level_score = LEVEL_MAPPING.get(
            log.get("level", "INFO"),
            1
        )

        message_length = len(
            log.get("message", "")
        )

        has_ip = 1 if log.get("ip_address") else 0

        features.append([
            level_score,
            message_length,
            has_ip
        ])

    dataframe = pd.DataFrame(
        features,
        columns=[
            "level_score",
            "message_length",
            "has_ip"
        ]
    )

    return dataframe