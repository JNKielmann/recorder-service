FROM python:3.10-bookworm as builder

RUN pip install poetry==1.8.2
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Install dependencies via poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

FROM python:3.10-bookworm
WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy app code
COPY recorder_service /app/recorder_service

# Copy test video
COPY data/test_video.mp4 /app/data/test_video.mp4
ENV LOCAL_VIDEO=/app/data/test_video.mp4

ENV STORAGE_DIR=/app/storage

# Start the server
EXPOSE 8080
CMD ["uvicorn", "recorder_service:app", "--host", "0.0.0.0", "--port", "8080"]


