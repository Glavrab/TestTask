FROM python:3.11-slim

# Prepare environment
ENV PYTHONPATH='/usr/src/test_task'
RUN adduser --disabled-password service
RUN chown -R service:service /usr/src
RUN chown -R service:service /usr/local
USER service
RUN mkdir /usr/src/test_task
WORKDIR /usr/src/test_task

# Install dependencies
RUN python -m pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-interaction --no-ansi

# Copy project files
COPY sources ./sources
COPY tests ./tests
COPY entrypoint.sh .

# Application entrypoint
ENTRYPOINT sh entrypoint.sh
