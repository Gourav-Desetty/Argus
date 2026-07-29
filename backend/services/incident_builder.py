from datetime import datetime
from typing import List, Dict

class IncidentBuilder:
    def build(
        self,
        raw_logs: List[str],
        parsed_logs: List[Dict],
        detection_result: Dict,
    ) -> Dict:

        return {
            "incident": detection_result["incident"],
            "severity": detection_result["severity"],
            "generated_at": datetime.now().isoformat(),

            "counts": detection_result["counts"],
            "messages": detection_result["messages"],

            "total_logs": len(raw_logs),

            "first_log_time": self._get_first_log_time(parsed_logs),
            "last_log_time": self._get_last_log_time(parsed_logs),

            "parsed_logs": parsed_logs,
            "raw_logs": raw_logs,
        }

    def _get_first_log_time(self, parsed_logs: List[Dict]):
        if not parsed_logs:
            return None

        return parsed_logs[0]["timestamp"]

    def _get_last_log_time(self, parsed_logs: List[Dict]):
        if not parsed_logs:
            return None

        return parsed_logs[-1]["timestamp"]