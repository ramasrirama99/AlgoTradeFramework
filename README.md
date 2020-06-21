# AlgoTradeFramework

### Background
AlgoTradeFramework is a python framework for creating and testing strategies for algorithmic trading locally.

### Requirements
python3, pgcopy, psycopg2, requests, schedule, setuptools
An AWS PostgreSQL DB instance


### Installation
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install libpq-dev

python3.6 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
pip install -e .
pip install -r requirements.txt
```

### Development
```
sudo service postgresql start
python backend/db/db_cacher.py
python backend/testers/back_tester.py
```

### Dataset
We make API calls to [AlphaVantage](https://www.alphavantage.co/documentation/) and store them in an AWS instance as well as a local backup database.

## Related papers
[1] Ian J. Goodfellow, Jonathon Shlens, [Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572)<br>
