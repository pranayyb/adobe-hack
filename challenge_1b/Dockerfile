FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends poppler-utils && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# COPY both folders relative to the build context (which is Adobe/)
COPY challenge_1a/ /app/challenge_1a/
COPY challenge_1b/ /app/challenge_1b/
COPY challenge_1b/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT ["python", "/app/challenge_1b/main.py"]
CMD ["--persona", "A software engineer with expertise in agile methodologies", \
    "--job", "Prepare a comprehensive analysis on agile testing methodologies, focusing on their evolution, current practices, and future trends"]
