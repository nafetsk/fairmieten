# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 #?
ENV PYTHONUNBUFFERED 1 #?
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory
WORKDIR /app

# Install dependencies
RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root
#RUN poetry run python3 manage.py migrate

# Copy the project code into the container
COPY . /app/
COPY main/.env.template main/.env

EXPOSE 8000

CMD poetry run python3 manage.py runserver
