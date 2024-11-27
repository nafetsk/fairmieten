## Get the code
```
git clone git@github.com:nafetsk/fairmieten.git
cd fairmieten
```

## Install Local:
```
python3 -m pip install poetry
poetry config virtualenvs.in-project true #optional
poetry install
poetry run python3 manage.py migrate
cp main/.env.template main/.env
edit .env -> choose a secret Secret
npx tailwindcss -i ./fairmieten/static/css/t_input.css -o ./fairmieten/static/css/t_output.css --watch
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
from aggregation.test_data import create_test_data
create_test_data()
```
to create testdata

## Test Aggregationen
open `localhost:8000/aggregationen` for a test bar graph

## Deploy Remote - with dokku  
(Get yourself a server)[https://kabelkopf.de/index.php/2024/11/26/ubuntu-server-setup/] and probably harden it a little bit.

```
# first ssh into your server
dokku apps:create fwfm 
dokku ports:add fwfm http:80:8001 
dokku domains:set fwfm **your_domain_name**

# from your local machine
# the remote username *must* be dokku or pushes will fail
cd fairmieten
git remote add <fairmieten> dokku@<your_domain_name>:fwfm
git push <fairmieten> main # or branchname:main if you are in another branch

# app should now be availeble under http://<your_domain_name>
# then got back to the server
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt:set --global email <your_email>
dokku letsencrypt:enable fwfm
# app should now be availeble under https://<your_domain_name> but with an error page

# now persist your database and enviroment variables
mkdir -p /data/fairmieten
sudo docker ps
sudo docker cp <container_id>:/app/main/.env /data/fairmieten/.env
touch /data/fairmieten/db.sqlite3

dokku storage:mount fwfm /data/fairmieten/.env:/app/main/.env
dokku storage:mount fwfm /data/fairmieten/db.sqlite3:/app/db.sqlite3

#than you have to set environment variables in the .env file
sudo apt install ne
ne /data/fairmieten/.env


# now restart your app
dokku ps:restart fwfm




```
