FROM python:3.11
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml ./
COPY . .
RUN uv sync --no-dev
CMD [ "uv", "run","--no-dev", "uvicorn", "radar_patient_check.main:app", "--host", "0.0.0.0" ]
