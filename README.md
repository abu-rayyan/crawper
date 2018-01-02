# CRAWPER
A python based crawler and scraper


## Getting Started
### Prerequisites
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [Postgres 10.1](https://www.postgresql.org/download/)

### Deployment

#### Configuring App
Follow these steps in order to deploy it correctly via Python VirtualEnviroment.
 1. Setup and configure [Python 2.7](https://www.python.org/download/releases/2.7/) and python-pip
 1. Install Virtual Enviroment globally
    ```bash
    pip install virtualenv
    ```
2. Create virtual enviroment for the app by navigating into app directory
    ```bash
    virtualenv venv
    ```
3. Activate the virtual enviroment
    ```bash
    sources venv/bin/activate
    ```
4. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```
4. Run main
    ```bash
    python main.py
    ```
#### Configuring Database
1. Download & Install [Postgres 10.1](https://www.postgresql.org/download/), set database name as postgres, username as postgres and password as postgres
2. Locate the database schema file "crawper_db_schema.sql" in project directory
3. Use Restore Database option in PgAdmin4 App to restore the database from schema file
    
## Build Using
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [PostgresSql 10.1](https://www.postgresql.org/download/)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [python requests](http://docs.python-requests.org/en/master/)

python -m textblob.download_corpora