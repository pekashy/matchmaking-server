FROM python:3.10-buster
RUN pip install Flask==2.2.2
RUN mkdir /code
COPY . /code

CMD ["python3", "/code/service.py"]