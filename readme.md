## Install:
```
python3 -m pip install poetry
poetry install
poetry run python3 manage.py migrate
```

## Start:
```
poetry run python3 manage.py runserver
```
open a browser an go to:
```
localhost:8000/hello?name=yourname
```

to see greetings to you.
