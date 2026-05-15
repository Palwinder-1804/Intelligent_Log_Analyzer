from datetime import datetime

from app.models.log_model import (
    raw_logs_collection,
    parsed_logs_collection
)

from app.services.rag.document_service import (
    create_log_document
)

from app.services.rag.chroma_service import (
    log_vector_store
)

from app.services.parsing.log_parser_service import parse_log_line


async def process_uploaded_log(
    filename: str,
    content_type: str,
    uploaded_by: str,
    file_content: str
):

    raw_log_document = {
        "filename": filename,
        "content_type": content_type,
        "uploaded_by": uploaded_by,
        "raw_content": file_content,
        "uploaded_at": datetime.utcnow()
    }

    raw_result = await raw_logs_collection.insert_one(
        raw_log_document
    )

    parsed_logs = []

    log_lines = file_content.splitlines()

    for line in log_lines:

        if not line.strip():
            continue

        parsed_log = parse_log_line(line)

        parsed_log["raw_log_id"] = str(
            raw_result.inserted_id
        )

        parsed_logs.append(parsed_log)
        
        document = create_log_document(parsed_log)
        log_vector_store.add_documents([document])

    if parsed_logs:
        await parsed_logs_collection.insert_many(
            parsed_logs
        )

    return {
        "raw_log_id": str(raw_result.inserted_id),
        "parsed_logs_count": len(parsed_logs)
    }