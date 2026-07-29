import os, time
from pathlib import Path
from fastapi import FastAPI, UploadFile, HTTPException
from backend.core.logger import logging, LOG_FILE_PATH
from backend.services.parser import Parser
from backend.services.detector import Detector
from backend.services.incident_builder import IncidentBuilder
from backend.services.prompt_builder import PromptBuilder
from backend.services.llm import LLMRouter
from agents.log_analysis_agent import LogAnalysisAgent

app = FastAPI()
detector = Detector()
parser = Parser()
builder = IncidentBuilder()
prompt_builder = PromptBuilder()
llm_router = LLMRouter()
log_analysis_agent = LogAnalysisAgent()

#------------------------------------Helper Functions--------------------------------#

def get_logs(path):
    with open(path, "r") as f:
        return f.readlines()

#-------------------------------------Dummy Routes------------------------------------#
@app.get('/login')
def login():
    logging.info("successfully logged in")
    return {"message": "Login successful"}

@app.get('/payment')
def payment():
    logging.error("payment failed")
    return {"message": "Payment failed"}

@app.get('/database')
def database():
    logging.critical("instance is not active")
    return {"message": "Database down"}

@app.get('/cache')
def cache():
    logging.warning("failed to retrieve cache")
    return {"message": "Cache miss"}


#------------------------------------Routes------------------------------------------#

@app.get('/')
def root():
    return{
        "message": "Argus is running"
    }

@app.get('/logs')
def logs():
    logs = get_logs(LOG_FILE_PATH)
    parsed_logs = parser.parse(logs)
    detection = detector.detect(parsed_logs)

    incident = builder.build(
        raw_logs=logs,
        parsed_logs=parsed_logs,
        detection_result=detection
    )

    state = {
        "incident": incident,
        "log_analysis": {},
        "root_cause": {},
        "report": {}
    }
    workflow = log_analysis_agent.graph()
    result = workflow.invoke(state)

    return {
        "result": result
    }