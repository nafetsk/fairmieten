## Install:
```
python3 -m pip install poetry
poetry config virtualenvs.in-project true #optional
poetry install
poetry run python3 manage.py migrate
cp main/.env.template main/.env
edit .env -> choose a secret Secret
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
