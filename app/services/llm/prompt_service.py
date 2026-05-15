from langchain_core.prompts import PromptTemplate


INCIDENT_PROMPT = PromptTemplate.from_template(
    """
    You are an intelligent incident analysis AI.

    Analyze the following logs and incident context.

    Historical Context:
    {context}

    User Query:
    {query}

    Explain:
    1. Probable root cause
    2. Severity level
    3. Affected services
    4. Suggested remediation
    5. Security risks if any

    Give a concise but technically accurate explanation.
    """
)