FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install paho-mqtt ddtrace datadog
CMD ["ddtrace-run","python","app.py"]