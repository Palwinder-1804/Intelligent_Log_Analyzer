def analyze_impact(parsed_logs):

    affected_services = set()

    severity = "LOW"

    critical_count = 0

    for log in parsed_logs:

        service = log.get("service")

        if service:
            affected_services.add(service)

        level = log.get("level")

        if level in ["ERROR", "CRITICAL"]:
            critical_count += 1

    if critical_count > 10:
        severity = "CRITICAL"
    elif critical_count > 5:
        severity = "HIGH"
    elif critical_count > 2:
        severity = "MEDIUM"

    return {
        "affected_services": list(affected_services),
        "severity": severity
    }