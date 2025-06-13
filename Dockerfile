# time_attack_game/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install flask requests matplotlib && \
    apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install pyjwt && \
    apt-get remove -y gcc python3-dev && apt-get autoremove -y

EXPOSE 5000
CMD ["python", "code.py"]  # Default to vulnerable version
