from typing import List

def detect_incidents(logs: List[dict]) -> dict:
    info = 0
    warning = 0
    error = 0
    critical = 0

    severity = "INFO"
    incident = False

    messages = []

    for log in logs:
        level = log["level"].upper()

        if level == "INFO":
            info += 1

        elif level == "WARNING":
            warning += 1
            messages.append(log["message"])

            if severity not in ["ERROR", "CRITICAL"]:
                severity = "WARNING"

        elif level == "ERROR":
            error += 1
            incident = True
            messages.append(log["message"])

            if severity != "CRITICAL":
                severity = "ERROR"

        elif level == "CRITICAL":
            critical += 1
            incident = True
            messages.append(log["message"])
            severity = "CRITICAL"

    return {
        "incident": incident,
        "severity": severity,
        "counts": {
            "INFO": info,
            "WARNING": warning,
            "ERROR": error,
            "CRITICAL": critical,
        },
        "messages": messages,
    }