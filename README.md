# Globus Auth backend for python-social-auth

Simple Django web application with Globus Auth backend for python-social-auth. The Globus Auth backend should also work with Flask, Pyramid, and other web framework supported by python-social-auth.



### Register a client

All clients need to register with Globus Auth and will receive a client id and secret. The following information is needed to complete the registration:



- Client name:



  This is displayed to the user on the consent screen. “<Client name> would like to” with a list of operations based on the scopes the client is asking.

- Scopes the client needs



   For all transfer operations, the scope to request is “urn:globus:auth:scope:transfer.api.globus.org:all”

  Other supported scopes:

  - urn:globus:auth:scope:auth.globus.org:view_identities



    Needed only for viewing private identities that is not the effective identity you have a token for; most clients won’t need this.

  - urn:globus:auth:scope:nexus.api.globus.org:groups



    Needed for Nexus groups

- Callback URLs (redirect URIs)



  The URL Globus should redirect the user to with the access token (must be HTTPS, TLS secured, does not necessarily have to be a valid certificate for testing servers)



  Python-social-auth uses Redirect URIs "https://<your_hostname>/complete/<backend>/". For the Globus Auth backend, the Redirect URI is "https://<your_hostname>/complete/globus/".

- GPG public key



  This will be used to secure the client secret that will be sent at registration

- Link to Terms and Conditions

- Link to Privacy Policy



Send a registration request with aforementioned information to support@globus.org. Once the registration is complete, Globus team will send a client id and secret (secured using the GPG key).



# Install psa-globus-auth

Create Python 2.7 virtual environment

```

$ python --version

Python 2.7.10

$ virtualenv venv

$ . venv/bin/activate

```

Install Django and python-social-auth

```

(venv)$ pip install django

(venv)$ pip install python-social-auth

```

Download psa-globus-auth

```

(venv)$ git clone git@github.com:lukaszlacinski/psa-globus-auth.git

```

Create the database

```

(venv)$ cd psa-globus-auth

(venv)$ ./manage.py migrate

```

Set SOCIAL_AUTH_GLOBUS_KEY and SOCIAL_AUTH_GLOBUS_SECRET in psa-globus/settings.py to a client id and secret received from Globus team.



# Apache/mod_wsgi

For example, on Ubuntu, add the following lines to /etc/apache2/sites-available/default-ssl.conf in `<VirtualHost _default_:443>`

```

WSGIDaemonProcess psa-globus python-path=<your_base_dir>/psa-globus-auth:<your_base_dir>/venv/lib/python2.7/site-packages

    WSGIProcessGroup psa-globus

    WSGIScriptAlias / <your_base_dir>/psa-globus-auth/psa-globus/wsgi.py process-group=psa-globus

    <Directory <your_base_dir>/psa-globus-auth/psa-globus>

        <Files wsgi.py>

            Require all granted

        </Files>

    </Directory>

```



Restart Apache and open https://<your_hostname>/ in a web browser. You will likely need to change owneship of the psa-globus-auth' directory to www-data (on Ubuntu), so Apache can run the code and create the SQLite3 database.
