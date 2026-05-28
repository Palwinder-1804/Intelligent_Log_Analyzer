from app.models.log_model import (
    parsed_logs_collection
)

from app.services.rca.timeline_service import (
    reconstruct_timeline
)

from app.services.rca.correlation_service import (
    correlate_incidents
)

from app.services.rca.impact_analysis_service import (
    analyze_impact
)

from app.services.rca.dependency_graph_service import (
    build_dependency_graph
)


async def analyze_root_cause(query: str):

    parsed_logs = []

    cursor = parsed_logs_collection.find().sort("_id", -1).limit(5000)

    async for log in cursor:

        parsed_logs.append(log)

    parsed_logs.reverse()

    correlated_logs = correlate_incidents(
        parsed_logs
    )

    timeline = reconstruct_timeline(
        correlated_logs
    )

    dependency_graph = build_dependency_graph(
        correlated_logs
    )

    impact_analysis = analyze_impact(
        correlated_logs
    )

    probable_root_cause = (
        correlated_logs[0]["message"]
        if correlated_logs
        else "No root cause identified"
    )

    failure_chain = list(
        dependency_graph.edges()
    )

    return {
        "query": query,
        "probable_root_cause": probable_root_cause,
        "timeline": timeline,
        "affected_services": impact_analysis[
            "affected_services"
        ],
        "severity": impact_analysis[
            "severity"
        ],
        "failure_chain": failure_chain
    }