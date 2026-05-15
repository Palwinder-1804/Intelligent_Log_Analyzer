from app.services.rag.retrieval_service import (
    retrieve_similar_logs
)

from app.services.llm.prompt_service import (
    INCIDENT_PROMPT
)

from app.services.llm.llm_service import (
    llm
)


async def run_rag_incident_chain(query: str):

    retrieved_docs = retrieve_similar_logs(
        query=query,
        k=5
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in retrieved_docs
        ]
    )

    prompt = INCIDENT_PROMPT.format(
        context=context,
        query=query
    )

    response = llm.invoke(prompt)

    return {
        "query": query,
        "retrieved_context": context,
        "explanation": response
    }