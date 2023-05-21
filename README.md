# simple-account-storage
A simple, web based, storage for your online accounts. Store username, password, URL and notes.

## Screenshot
![Screenshot 2023-05-21 215714](https://github.com/lorenzocampanile/simple-account-storage/assets/17176752/270a6843-f1a2-40b9-9d0f-67609f9adb4c)

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
6. Add your users and their associated accounts: `http://127.0.0.1:8000/admin/`
7. Go to page: `http://127.0.0.1:8000/accounts/`
