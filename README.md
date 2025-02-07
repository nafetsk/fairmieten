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
npm install
npx tailwindcss -i ./fairmieten/static/css/t_input.css -o ./fairmieten/static/css/t_output.css --watch
poetry run python3 manage.py createsuperuser
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
(Get yourself a server)[https://kabelkopf.de/index.php/2024/11/26/ubuntu-server-setup/] probably harden it a little bit.
SSH to that server and follow the Quick start instructions at (dokku.com)[https://dokku.com/]
use <your_domain> instead of dokku.me (could be second or thrid level domain)

```
# proceed on remote server
dokku apps:create fwfm #if not already done
dokku ports:add fwfm http:80:8001 
dokku domains:set fwfm <your_app_domain> #optional if not set fwfm.<your_domain> is used

# add your ssh key
# first copy your public key to the server for example with
scp ~/.ssh/id_rsa.pub dokku@<your_domain>:/home/dokku/.ssh/id_rsa.pub
# the add the key to dokku	
dokku ssh-keys:add KEY_NAME path/to/id_rsa.pub

# and persist your database and enviroment variables
mkdir -p /data/fairmieten
sudo docker volume create "fairmieten"   --driver "local"   --opt "type=none"   --opt "device=/data/fairmieten"   --opt "o=bind"
dokku storage:mount fwfm fairmieten:/app/data


# from your local machine
# the remote username *must* be dokku or pushes will fail
cd fairmieten
git remote add <fairmieten> dokku@<your_domain>:fwfm #ip is also possible
git push <fairmieten> main # or branchname:main if you are in another branch

# app should now be available under http://<your_app_domain>
# then got back to the server
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt:set --global email <your_email>
dokku letsencrypt:enable fwfm
# app should now be available under https://<your_app_domain> but with an error page


#than you have to set environment variables in the .env file
sudo apt install ne
ne /data/fairmieten/env_variables/.env
# and create a superuser
dokku enter fwfm web poetry run python3 manage.py createsuperuser

# now restart your app
dokku ps:restart fwfm

# app should now be available under https://<your_app_domain> 

```
