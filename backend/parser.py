import re

def parse_logs(log_lines):
    result = []
    for log in log_lines:
        match = re.search(
            r"\[(.*?)\]\s+(\d+)\s+(\S+)\s+-\s+(\w+)\s+-\s+(.*)",
            log,
        )
        if match:
            result.append({
                "timestamp": match.group(1),
                "line": match.group(2),
                "logger": match.group(3),
                "level": match.group(4),
                "message": match.group(5),
            })

    return result
