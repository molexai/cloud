FROM ubuntu:latest AS base
LABEL authors="molexAI"
ENTRYPOINT ["top", "-b"]
FROM python:3.12-alpine
COPY requirements.txt /molexcloud/
RUN pip install --no-cache-dir -r /molexcloud/requirements.txt
WORKDIR /molexcloud
COPY /molexcloud /molexcloud
CMD ["python", "main.py"]