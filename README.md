# SoftDesk-API

#### Require repository

```sh
git clone https://github.com/AlxandrV/SoftDesk-API.git ./
```

#### Create a virtual environnement

```sh
python -m venv env
```

#### Execute virtual env

For Windows
```sh
source env/Scripts/activate
```

For Linux
```sh
source env/bin/activate
```

#### Add requirements

```sh
pip install -r requirements.txt
```

## Django

#### Migrate models

```sh
python SoftDesk/manage.py makemigrations
```

```sh
python SoftDesk/manage.py migrate
```

#### Launch server

```sh
python SoftDesk/manage.py runserver
```