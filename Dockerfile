FROM python:3.11-slim
WORKDIR /workspace
COPY . .
RUN pip install uv
