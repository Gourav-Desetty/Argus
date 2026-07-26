from datetime import datetime
from typing import List, Dict


def build_incident(
    raw_logs: List[str],
    parsed_logs: List[Dict],
    detection_result: Dict
) -> Dict:

    incident = {
        "incident": detection_result["incident"],
        "severity": detection_result["severity"],
        "generated_at": datetime.now().isoformat(),

        "counts": detection_result["counts"],
        "messages": detection_result["messages"],

        "total_logs": len(raw_logs),

        "first_log_time": (
            parsed_logs[0]["timestamp"]
            if parsed_logs else None
        ),

        "last_log_time": (
            parsed_logs[-1]["timestamp"]
            if parsed_logs else None
        ),

        "parsed_logs": parsed_logs,

        "raw_logs": raw_logs
    }

    return incident