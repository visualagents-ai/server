FROM ubuntu:latest
LABEL maintainer="test"
ENV GROUP_ID=1000 \
    USER_ID=1000
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates supervisor procps cron python3.12-venv python3-gdbm wget gnupg unzip curl
RUN mkdir /opt/visualagents
WORKDIR /opt/visualagents
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python3 -m venv venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN ["venv/bin/python3", "-m", "pip", "install", "--upgrade", "pip", "wheel"]
RUN apt-get install -y  python3-wheel
COPY requirements.txt requirements.txt
RUN ["venv/bin/python3", "-m", "pip", "install", "--no-cache-dir", "--upgrade", "-r", "requirements.txt"]
COPY api/api.py api.py
EXPOSE 8000:8000
CMD ["venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "api:app"]


