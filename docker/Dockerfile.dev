ARG PYTHON
FROM python:${PYTHON}

WORKDIR /app
COPY . /app


RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 zbar-tools  -y
RUN pip install -e .

ENTRYPOINT ["coronacheck-tools"]