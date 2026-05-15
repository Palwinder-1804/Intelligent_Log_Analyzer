def clean_logs(logs):

    cleaned_logs = []

    for log in logs:

        log = log.strip()

        if not log:
            continue

        cleaned_logs.append(log)

    return cleaned_logs