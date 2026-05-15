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