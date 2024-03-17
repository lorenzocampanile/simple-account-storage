# simple-account-storage
A simple, web based, storage for your online accounts. Store username, password, URL, notes and more. Suitable also for storing your databases and SSH servers credentials.

## Screenshot
![Screenshot 2023-05-21 220129](https://github.com/lorenzocampanile/simple-account-storage/assets/17176752/26806b3e-70c5-4e4f-ae71-830f2a073e9f)

## Installation
1. Clone this project: `git clone https://github.com/lorenzocampanile/simple-account-storage.git`
1. Create the configuration file:
```
    cd simple-account-storage
    printf "[baseconfig]\nDEBUG = false\nSECRET_KEY = your_secret_key\nENCRYPTION_KEY_SALT = your_salt\nALLOWED_HOSTS = mydomail.com\nCSRF_TRUSTED_ORIGINS = https://mydomail.com\nFRONTEND_BASE_URL = https://mydomail.com" > simpleaccountstorage.conf
```
1. Install the dependencies:
```
    python -m venv env
    env/bin/pip install -r requirements.txt
    env/bin/python manager.py runserver
    cd web-client
    npm install
    echo "VITE_BASE_API_URL=https://mydomail.com" > .env
    npm run build
    cd ..
```
1. Collect static files: `env/bin/python manage.py collectstatic`
1. Run the project: `env/bin/gunicorn simpleaccountstorage.wsgi # probably you want this under systemd or similar`
1. Configure your webserver to:
* serve the `static-root` folder directly (optional, but highly reccomended)
* proxy_pass all `/api` requests to gunicorn web server
1. Go to page: `https://mydomail.com`

## Run for development
1. Create the configuration file:
```
printf "[baseconfig]\nDEBUG = true\nSECRET_KEY = your_secret_key\nENCRYPTION_KEY_SALT = your_salt\nALLOWED_HOSTS = 127.0.0.1,myenrironment.local\nCSRF_TRUSTED_ORIGINS = http://127.0.0.1:5173\nFRONTEND_BASE_URL = http://127.0.0.1:5173" > simpleaccountstorage.conf
```
1. Run the Django backend server: `python manage.py runserver`
1. Run the web client NPM server: `cd web-client`, `echo "VITE_BASE_API_URL=http://127.0.0.1:8000" > .env` and `npm run dev`
1. Run Mailhog (optional, if using emails): `mailhog -api-bind-addr 127.0.0.1:8080 -ui-bind-addr 127.0.0.1:8080`
