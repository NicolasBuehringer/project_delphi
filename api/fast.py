from project_delphi.scheduler import run_app

# $DELETE_BEGIN
from datetime import datetime
import pytz

import pandas as pd
import joblib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"AFD" :11.61, "CDU":21.47,  "FDP":10.83,  "GRUENE":19.19, "LINKE":7.61, "SPD": 15.36, "OTHER" : 10.76 }

@app.post("/run_app/")
def execute_function(start_time=None, end_time=None):
    run_app(start_time, end_time)
    return "This finished"
    #run_app(start_time, end_time)
