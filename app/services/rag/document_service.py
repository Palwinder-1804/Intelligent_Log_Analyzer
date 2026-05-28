from langchain_core.documents import Document


def create_log_document(parsed_log):

    content = f"""
    Timestamp: {parsed_log.get("timestamp")}

    Level: {parsed_log.get("level")}

    Service: {parsed_log.get("service")}

    Message: {parsed_log.get("message")}

    IP Address: {parsed_log.get("ip_address")}
    """

    metadata = {
        "source": "uploaded_logs",
        "service": parsed_log.get("service"),
        "level": parsed_log.get("level"),
        "raw_log_id": parsed_log.get("raw_log_id")
    }

    return Document(
        page_content=content,
        metadata=metadata
    )


def create_log_chunk_document(parsed_logs_chunk, raw_log_id):
    lines = []
    services = set()
    levels = set()

    for log in parsed_logs_chunk:
        ts = log.get("timestamp") or "-"
        lvl = log.get("level") or "-"
        svc = log.get("service") or "-"
        msg = log.get("message") or "-"
        ip = log.get("ip_address") or "-"
        
        lines.append(f"[{ts}] [{lvl}] [{svc}] {msg} (IP: {ip})")
        if log.get("service"):
            services.add(log.get("service"))
        if log.get("level"):
            levels.add(log.get("level"))

    content = "\n".join(lines)
    primary_service = list(services)[0] if services else "unknown"
    primary_level = list(levels)[0] if levels else "unknown"

    metadata = {
        "source": "uploaded_logs",
        "service": primary_service,
        "level": primary_level,
        "raw_log_id": raw_log_id
    }

    return Document(
        page_content=content,
        metadata=metadata
    )