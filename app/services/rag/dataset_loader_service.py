import os


def load_log_dataset(dataset_path, max_lines: int = None):

    logs = []
    total_lines = 0

    for root, _, files in os.walk(dataset_path):

        for file in files:

            if file.endswith((".log", ".txt")):

                full_path = os.path.join(root, file)

                with open(
                    full_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    for line in f:
                        logs.append(line)
                        total_lines += 1
                        if max_lines and total_lines >= max_lines:
                            return logs

    return logs