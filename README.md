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


## Testdaten

You can open the interactive shell with
```
poetry run python3 manage.py shell
```
Then run 
```
from fairmieten.test_data import create_test_data
create_test_data()
```
to create testdata

## Test Aggregationen
open `localhost:8000/aggregationen` for a test bar graph