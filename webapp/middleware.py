from django.shortcuts import redirect
from django.urls import reverse
from social_core.exceptions import AuthForbidden


class GlobusAuthExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, AuthForbidden):
            return
        if not isinstance(exception.args, tuple):
            return
        if not isinstance(exception.args[0], dict):
            return

        kwargs = exception.args[0]

        session_message = kwargs.get('session_message')
        session_required_identities = kwargs.get('session_required_identities')
        if session_message and session_required_identities:
            strategy = exception.backend.strategy
            strategy.session_set('session_message', session_message)
            strategy.session_set('session_required_identities', session_required_identities)
            return redirect(reverse('social:begin', kwargs={'backend': 'globus'}))

        group_name = kwargs.get('group_name')
        group_join_url = kwargs.get('group_join_url')
        if group_name and group_join_url:
            return redirect(group_join_url)
