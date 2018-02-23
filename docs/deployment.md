### Deploying the Project
Follow these steps in order to deploy it correctly via Python VirtualEnviroment.
 1. Setup and configure [Python 2.7](https://www.python.org/download/releases/2.7/) and python-pip
 2. Install NLP lib requirements 
    ```python
        pip install textblob
        python -m textblob.download_corpora
    ```
 3. Install Virtual Enviroment globally
    ```bash
        pip install virtualenv
    ```
4. Create virtual enviroment for the app by navigating into app directory
    ```bash
       virtualenv venv
    ```
5. Activate the virtual enviroment
    ```bash
       sources venv/bin/activate
    ```
6. Install the required packages
    ```bash
       pip install -r requirements.txt
    ```
7. Run setup.py using
    ```python
       python setup.py build
       python setup.py install
    ```
8. Running Scraper
    ```python
       python main.py
    ```
9. Running Server
    ```python
       python server/run.py
    ```