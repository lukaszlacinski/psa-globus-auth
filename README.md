# Globus Auth backend for Python Social Auth

Simple Django web application with Globus Auth backend for Python Social Auth. The Globus Auth backend should also work with Flask, Pyramid, and other web framework supported by Python Social Auth.

## Install psa-globus-auth

Create Python 3.x virtual environment
```
$ python --version
Python 3.7.15
$ python -mvenv  venv
$ . venv/bin/activate
```
Download and install psa-globus-auth with all required Python packages (Django, Python Social Auth, etc.)
```
(venv)$ git clone git@github.com:lukaszlacinski/psa-globus-auth.git
(venv)$ cd psa-globus-auth
(venv)$ pip install -r requirements.txt
```
Create the database
```
(venv)$ ./manage.py migrate
```
## Register a client

All OAuth2 clients need to register with Globus Auth to get a client id and secret. To register your client, go to `https://developers.globus.org/`, click 'Register your app with Globus', add a new project and add a new app in the project. Enter a name of your app you want to be shown to users when they are asked for a consent when redirected to Globus Auth for authentication. Select the following scopes: `openid`, `email`, `profile`, and if your application is going to use the Globus Transfer service, select `urn:globus:auth:scope:transfer.api.globus.org:all` as well. Enter the redirect URI: `https://example.com/<prefix>/complete/globus/`, where `<prefix>` is a root path to your application. If your web server does not serve any other web apps or web pages you can skip `<prefix>` (`https://example.com/complete/globus/`). Click 'Create App'. Click 'Generate New Client Secret' and copy Client ID and a generated secret to `webapp/settings.py` as `SOCIAL_AUTH_GLOBUS_KEY` and `SOCIAL_AUTH_GLOBUS_SECRET`.

## Apache/mod_wsgi

For example, on Ubuntu, add the following lines to /etc/apache2/sites-available/default-ssl.conf in `<VirtualHost _default_:443>`
```
    WSGIDaemonProcess globusapp user=<your_username> python-path=<your_base_dir>/psa-globus-auth python-home=<your_base_dir>/venv
    WSGIScriptAlias /<prefix> <your_base_dir>/psa-globus-auth/webapp/wsgi.py process-group=globusapp
    <Directory <your_base_dir>/psa-globus-auth/webapp>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
```
Restart Apache and open `https://example.com/<prefix>` in a web browser. If you do not own `example.com` domain, you may need to add:
```
127.0.0.1 example.com
```
to your `/etc/hosts`.

