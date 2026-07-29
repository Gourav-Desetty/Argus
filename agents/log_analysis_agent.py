import json
from typing import TypedDict
from langgraph.graph import START, END, StateGraph
from backend.services.llm import LLMRouter
from backend.services.prompt_builder import PromptBuilder

class AgentState(TypedDict):
    incident: dict
    log_analysis: dict
    root_cause: dict
    report: dict

class LogAnalysisAgent:
    def __init__(self) -> None:
        self.llm_router = LLMRouter()
        self.prompt_builder = PromptBuilder()

    def analyze_logs(self, state: AgentState) -> AgentState:
        incident = state['incident']
        prompt = self.prompt_builder.analyze_logs(incident=incident)
        response = json.loads(self.llm_router.analyze_logs(prompt=prompt))

        return {
            **state,
            "log_analysis": {
                "service": response["service"],
                "critical_errors": response["critical_errors"],
                "summary": response["summary"],
                "evidence": response["evidence"],
            }
        }

    def root_cause(self, state: AgentState):
        incident = state["incident"]
        prompt = self.prompt_builder.root_cause(incident=incident, state=state)
        response = json.loads(self.llm_router.analyze_root_cause(prompt=prompt))

        return {
            **state,
            "root_cause": {
                "cause": response['cause'],
                "confidence": response['confidence'],
                "missing_evidence": response['missing_evidence'],
                "recommendation": response['recommendation']
            }
        }

    def generate_report(self, state: AgentState):
        incident = state["incident"]
        prompt = self.prompt_builder.generate_report(incident=incident, state=state)
        response = self.llm_router.generate_report(prompt=prompt)

        return {
            **state,
            "report": {
                "incident_summary": response["incident_summary"],
                "executive_summary": response["executive_summary"],
                "recommended_actions": response["recommended_actions"],
                "jira_description": response["jira_description"],
                "slack_message": response["slack_message"]
            }
        }

    def graph(self):
        graph = StateGraph(AgentState)

        graph.add_node('analyze_logs', self.analyze_logs)
        graph.add_node('root_cause', self.root_cause)
        graph.add_node('generate_report', self.generate_report)

        graph.add_edge(START, 'analyze_logs')
        graph.add_edge('analyze_logs', 'root_cause')
        graph.add_edge('root_cause', 'generate_report')
        graph.add_edge('generate_report', END)

        workflow = graph.compile()

        return workflow