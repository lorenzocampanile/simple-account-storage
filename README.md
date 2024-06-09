# simple-account-storage
A simple, web based, storage for your online accounts. Store username, password, URL, notes and more. Suitable also for storing your databases and SSH servers credentials.

## Screenshot
![Screenshot 2023-05-21 220129](https://github.com/lorenzocampanile/simple-account-storage/assets/17176752/26806b3e-70c5-4e4f-ae71-830f2a073e9f)

## Installation
1. Clone this project
1. Create a Python virtual environment and activate it: `python -m venv env/ && source env/bin/activate`
1. Install the backend dependencies: `pip install -r requirements.txt`
1. Install the frontend dependencies: `cd web-client && npm install && cd ..`
1. Execute the database migrations (SQLite): `python manage.py migrate`

## Run for development
1. Create the configuration file, in the project root folder:
    - ```cd simple-account-storage```
    - Paste the follwing in a new `simpleaccountstorage.conf` file:
    ```
    [baseconfig]
    DEBUG = true
    SECRET_KEY = your_secret_key  ; Generate one using the following command: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
    ENCRYPTION_KEY_SALT = your_salt  ; Generate one using the following command: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
    ALLOWED_HOSTS = localhost
    CSRF_TRUSTED_ORIGINS = http://localhost:5173
    FRONTEND_BASE_URL = http://localhost:5173
    LOG_FILENAME = ./error.log
    ```
1. Create the configuration file, in the web client folder
    - ```echo "VITE_BASE_API_URL=http://localhost:8000" > web-client/.env```

1. Run the Django backend server: `python manage.py runserver`
1. Run the web client NPM server: `cd web-client && npm run dev`
1. Run Mailhog: `mailhog -api-bind-addr 127.0.0.1:8080 -ui-bind-addr 127.0.0.1:8080`
1. Go to page http://127.0.0.1:5173

## Run for production
1. Create the configuration file, in the project root folder:
    - ```cd simple-account-storage```
    - Paste the follwing in a new `simpleaccountstorage.conf` file:
    ```
    [baseconfig]
    DEBUG = false
    SECRET_KEY = your_secret_key  ; Generate one using the following command: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
    ENCRYPTION_KEY_SALT = your_salt  ; Generate one using the following command: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
    ALLOWED_HOSTS = mydomail.com  ; comma separated list of domains
    CSRF_TRUSTED_ORIGINS = https://mydomail.com  ; comma separated list of URLs
    FRONTEND_BASE_URL = https://mydomail.com  
    LOG_FILENAME = /var/log/simple-account-storage/error.log
    EMAIL_HOST = your_smtp_host
    EMAIL_PORT = your_smtp_port
    EMAIL_HOST_USER = your_smtp_user
    EMAIL_HOST_PASSWORD = your_smtp_password
    EMAIL_USE_TLS = true  ; depending on your SMTP provider
    EMAIL_TIMEOUT = 5
    EMAIL_FROM = smpt_user  ; depending on your SMTP provider
    SERVER_EMAIL = server_email  ; depending on your SMTP provider, it's the "From" header in admin emails
    ```
1. Create the configuration file, in the web client folder
    - ```cd web-client/```
    - ```echo "VITE_BASE_API_URL=https://mydomail.com" > .env```
1. Build the frontend client:
    - ```cd web-client/```
    - ```npm run build```
1. Create the folder for the error log file `mkdir /var/log/simple-account-storage/` and ensure writing permission are granted
1. Collect static files: `env/bin/python manage.py collectstatic`
1. Run the project: `env/bin/gunicorn simpleaccountstorage.wsgi # probably you want this under systemd or similar and optimize the gunicorn workers according to your needs`
1. Configure your webserver to:
* serve the `static-root` folder directly (optional, but highly reccomended)
* proxy_pass all `/api` requests to gunicorn web server
1. Go to page: `https://mydomail.com`