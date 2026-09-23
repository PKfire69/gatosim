FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir ruff==0.15.1
COPY pyproject.toml world_model_starter.py test_world_model_starter.py ./

CMD ["python", "world_model_starter.py"]
