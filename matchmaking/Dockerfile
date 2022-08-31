FROM python:3.10-buster
COPY matchmaking/requirements.txt .
RUN pip install -r requirements.txt
COPY matchmaking/. .
COPY schemas schemas

CMD ["python3", "service.py"]