def chunk_logs(
    logs,
    chunk_size=10
):

    chunks = []

    for i in range(0, len(logs), chunk_size):

        chunk = logs[i:i + chunk_size]

        chunks.append(chunk)

    return chunks