## Flask SQLAlchemy DEMO

this project is a DEMO application using flask and mysql using SQLAlchemy

### Installation with docker-compose

```
git clone https://github.com/adriavend/flask-sqlalchemy
cd flask-sqlalchemy
docker-compose up
```

### Manual Installation

##### Requirements

* Python3
* Mysql

before run the app you must change the following configuration in config.py:

```
SQLALCHEMY_DATABASE_URI
```

```
git clone https://github.com/adriavend/flask-sqlalchemy
cd flask-sqlalchemy
pip install -r requirements.txt
python main.py
```
