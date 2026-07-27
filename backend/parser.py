import re
from typing import List, Dict


class Parser:
    LOG_PATTERN = re.compile(
        r"\[(.*?)\]\s+(\d+)\s+(\S+)\s+-\s+(\w+)\s+-\s+(.*)"
    )
    def parse(self, log_lines: List[str]) -> List[Dict]:\

        parsed_logs = []

        for log in log_lines:
            parsed_log = self._parse_log(log)

            if parsed_log:
                parsed_logs.append(parsed_log)

        return parsed_logs

    def _parse_log(self, log: str) -> Dict | None:

        match = self.LOG_PATTERN.search(log)

        if not match:
            return None

        return {
            "timestamp": match.group(1),
            "line": match.group(2),
            "logger": match.group(3),
            "level": match.group(4),
            "message": match.group(5),
        }