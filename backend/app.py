import os, time
from pathlib import Path
from fastapi import FastAPI, UploadFile, HTTPException
from backend.logger import logging, LOG_FILE_PATH
from backend.parser import parse_logs
from backend.detector import detect_incidents
from backend.incident_builder import build_incident

app = FastAPI()

#------------------------------------Helper Functions--------------------------------#

def get_logs(path):
    with open(path, "r") as f:
        return f.readlines()

#------------------------------------Routes------------------------------------------#
@app.get('/')
def root():
    return{
        "message": "Argus is running"
    }


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
#-------------------------------------------------------------------------------------#

@app.get('/logs')
def logs():
    logs = get_logs(LOG_FILE_PATH)
    parsed_logs = parse_logs(logs)
    detection = detect_incidents(parsed_logs)

    incident = build_incident(
        raw_logs=logs,
        parsed_logs=parsed_logs,
        detection_result=detection
    )

    return {
        "output": incident
    }