import os, json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr


load_dotenv()

GROQ_API_KEY = SecretStr(os.environ["GROQ_API_KEY"])


class LLMRouter:
    def __init__(self) -> None:
        # Triage: high-volume, low-complexity classification
        self.fast = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0.1,
        )

        # Root-cause analysis: low-volume, needs real reasoning
        self.reasoning = ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=GROQ_API_KEY,
            temperature=0.2,
        )

        # Structured report generation: schema adherence over depth
        self.structured = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0.0,
        )

        # Slack/Jira message drafting: natural prose
        self.draft = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=GROQ_API_KEY,
            temperature=0.4,
        )

        # Safety/content moderation gate before external posting
        self.safety = ChatGroq(
            model="openai/gpt-oss-safeguard-20b",
            api_key=GROQ_API_KEY,
            temperature=0.0,
        )

    def triage(self, prompt: str) -> str:
        return self.fast.invoke(prompt).content

    def analyze_root_cause(self, prompt: str) -> str:
        return self.reasoning.invoke(prompt).content

    def draft_message(self, prompt: str) -> str:
        return self.draft.invoke(prompt).content

    def moderate(self, prompt: str) -> str:
        return self.safety.invoke(prompt).content

    def generate_report(self, prompt):
        response = self.structured.invoke(prompt).content
        return json.loads(response)

    def analyze_logs(self, prompt) -> dict:
        return self.fast.invoke(prompt).content
