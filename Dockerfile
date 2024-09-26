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

# Copy the project code into the container
COPY . /app/
COPY main/.env.template main/.env
RUN poetry run python3 manage.py migrate
RUN poetry run python manage.py shell -c "from fairmieten.test_data import create_test_data; create_test_data()"

EXPOSE 8001

ENTRYPOINT ["poetry", "run", "python3" ,"manage.py", "runserver"]
CMD ["0.0.0.0:8001"]
