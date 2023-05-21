# simple-account-storage
A simple, web based, storage for your online accounts. Store username, password, URL and notes.

## Installation
1. Clone this project: `git clone https://github.com/lorenzocampanile/simple-account-storage.git`
2. Create the configuration file:
```
    cd simple-account-storage
    printf "[baseconfig]\nDEBUG = false\nSECRET_KEY = your_secret_key\nENCRYPTION_KEY = another_secret_key\nALLOWED_HOSTS = 127.0.0.1,myenrironment.local" > simpleaccountstorage.conf
```
3. Install the dependencies:
```
    python -m venv env
    env/bin/pip install -r requirements.txt
    env/bin/python manager.py runserver
```
4. Create the superuser, for managing users and accounts: `env/bin/python manage.py createsuperuser`
5. Run the project: `env/bin/python manage.py runserver`
6. Go to page: `http://127.0.0.1:8000/accounts/`
