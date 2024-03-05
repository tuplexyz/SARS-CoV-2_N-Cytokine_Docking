# app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install -r /app/vis_app/requirements.txt

EXPOSE 8501

WORKDIR /app/vis_app

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Protein_Viewer.py", "--server.port=8501", "--server.address=0.0.0.0"]