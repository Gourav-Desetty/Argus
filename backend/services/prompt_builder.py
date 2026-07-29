import json
from langchain_core.prompts import ChatPromptTemplate
from backend.prompts.incident_prompt import INCIDENT_ANALYSIS_PROMPT
from backend.prompts.log_analysis_prompt import LOG_ANALYSIS_PROMPT
from backend.prompts.root_cause_prompt import ROOT_CAUSE_PROMPT
from backend.prompts.report_prompt import REPORT_PROMPT

class PromptBuilder:
    def incident_analysis(self, incident: dict) :
        prompt = ChatPromptTemplate.from_template(
            INCIDENT_ANALYSIS_PROMPT
        )

        parsed_log_lines = "\n".join(
            f"[{log['timestamp']}] {log['logger']} - "
            f"{log['level']} - {log['message']}"
            for log in incident["parsed_logs"]
        )

        messages = prompt.invoke(
            {
                "severity": incident["severity"],
                "generated_at": incident["generated_at"],
                "total_logs": incident["total_logs"],
                "first_log_time": incident["first_log_time"],
                "last_log_time": incident["last_log_time"],
                "counts": json.dumps(incident["counts"], indent=2),
                "parsed_log_lines": parsed_log_lines,
            }
        )
        return messages

    def analyze_logs(self, incident: dict):
        prompt = ChatPromptTemplate.from_template(LOG_ANALYSIS_PROMPT)

        parsed_log_lines = "\n".join(
            f"[{log['timestamp']}] {log['logger']} - "
            f"{log['level']} - {log['message']}"
            for log in incident["parsed_logs"]
        )

        return prompt.invoke(
            {
                "severity": incident["severity"],
                "generated_at": incident["generated_at"],
                "total_logs": incident["total_logs"],
                "first_log_time": incident["first_log_time"],
                "last_log_time": incident["last_log_time"],
                "counts": json.dumps(incident["counts"], indent=2),
                "parsed_log_lines": parsed_log_lines,
            }
        )

    def root_cause(self, incident: dict, state: dict):
        prompt = ChatPromptTemplate.from_template(ROOT_CAUSE_PROMPT)

        parsed_log_lines = "\n".join(
            f"[{log['timestamp']}] {log['logger']} - "
            f"{log['level']} - {log['message']}"
            for log in incident["parsed_logs"]
        )

        return prompt.invoke(
            {
                "severity": incident["severity"],
                "generated_at": incident["generated_at"],
                "total_logs": incident["total_logs"],
                "first_log_time": incident["first_log_time"],
                "last_log_time": incident["last_log_time"],
                "counts": json.dumps(incident["counts"], indent=2),
                "parsed_log_lines": parsed_log_lines,
                "service": state["log_analysis"]["service"],
                "critical_errors": json.dumps(
                    state["log_analysis"]["critical_errors"],
                    indent=2,
                ),
                "log_summary": state["log_analysis"]["summary"],
                "log_evidence": json.dumps(
                    state["log_analysis"]["evidence"],
                    indent=2,
                )
            }
        )

    def generate_report(self, incident:dict, state: dict):
        prompt = ChatPromptTemplate.from_template(REPORT_PROMPT)

        parsed_log_lines = "\n".join(
            f"[{log['timestamp']}] {log['logger']} - "
            f"{log['level']} - {log['message']}"
            for log in incident["parsed_logs"]
        )

        return prompt.invoke(
            {
                "severity": incident["severity"],
                "generated_at": incident["generated_at"],
                "total_logs": incident["total_logs"],
                "first_log_time": incident["first_log_time"],
                "last_log_time": incident["last_log_time"],
                "counts": json.dumps(incident["counts"], indent=2),
                "parsed_log_lines": parsed_log_lines,
                "service": state["log_analysis"]["service"],
                "critical_errors": json.dumps(
                    state["log_analysis"]["critical_errors"],
                    indent=2,
                ),
                "log_summary": state["log_analysis"]["summary"],
                "log_evidence": json.dumps(
                    state["log_analysis"]["evidence"],
                    indent=2,
                ),
                "cause": state["root_cause"]["cause"],
                "confidence": state["root_cause"]["confidence"],
                "missing_evidence": json.dumps(
                    state["root_cause"]["missing_evidence"],
                    indent=2,
                ),
                "root_cause_recommendations": json.dumps(
                    state["root_cause"]["recommendation"],
                    indent=2,
                ),
            }
        )