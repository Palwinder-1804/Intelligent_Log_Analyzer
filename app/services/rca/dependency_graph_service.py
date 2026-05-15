import networkx as nx


dependency_graph = nx.DiGraph()


def build_dependency_graph(parsed_logs):

    services = []

    for log in parsed_logs:

        service = log.get("service")

        if service:
            services.append(service)

    for i in range(len(services) - 1):

        source = services[i]
        target = services[i + 1]

        dependency_graph.add_edge(
            source,
            target
        )

    return dependency_graph