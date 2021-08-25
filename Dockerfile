FROM python:3.8.6-buster

COPY api /api
COPY project_delphi /project_delphi
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt
COPY /home/lucab/code/Lucaqberra/gcp/project-delphi-323909-c243cef634c6.json /credentials.json

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
