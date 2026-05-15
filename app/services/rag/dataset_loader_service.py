import os


def load_log_dataset(dataset_path):

    logs = []

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

                    logs.extend(f.readlines())

    return logs