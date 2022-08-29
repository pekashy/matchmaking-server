FROM python:3.10-buster
COPY client/requirements.txt .
RUN pip install -r requirements.txt
COPY client/. .
COPY schemas schemas

CMD ["python3", "service.py"]