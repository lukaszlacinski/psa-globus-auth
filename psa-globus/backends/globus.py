"""
Globus Auth backend, docs at:
    https://docs.globus.org/api/auth
"""

from social.backends.oauth import BaseOAuth2
from social.p3 import urlencode, unquote

from jwt import DecodeError, ExpiredSignature, decode as jwt_decode


class GlobusOAuth2(BaseOAuth2):
    name = 'globus'
    AUTHORIZATION_URL = 'https://auth.globus.org/v2/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://auth.globus.org/v2/oauth2/token'
    DEFAULT_SCOPE = ['urn:globus:auth:scope:transfer.api.globus.org:all']
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('access_token', 'access_token', True),
        ('expires_in', 'expires_in', True),
        ('id_token', 'id_token', True),
        ('refresh_token', 'refresh_token', True)
    ]


    # PSA does not encode redirect_uri if REDIRECT_STATE=False
    def auth_url(self):
        """Return redirect url"""
        state = self.get_or_create_state()
        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())
        params = urlencode(params)
        return '{0}?{1}'.format(self.authorization_url(), params)


    # extract user info from id_token (OpenID Connect)
    def user_data(self, access_token, *args, **kwargs):
        response = kwargs.get('response')
        id_token = response.get('id_token')
        try:
            decoded_id_token = jwt_decode(id_token, verify=False)
        except (DecodeError, ExpiredSignature) as de:
            raise AuthTokenError(self, de)
        return {'uid': decoded_id_token.get('sub'),
                'username': decoded_id_token.get('preferred_username'),
                'name': decoded_id_token.get('name'),
                'email': decoded_id_token.get('email')
                }


    def get_user_details(self, response):
        name = response.get('name') or ''
        fullname, first_name, last_name = self.get_user_names(name)
        return {'username': response.get('username'),
                'email': response.get('email'),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}


    def get_user_id(self, details, response):
        return response['uid']



