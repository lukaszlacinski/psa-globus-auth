from django.shortcuts import render


def get_token(tokens, scope):
    for item in tokens:
        if scope == item.get("scope"):
            return item.get("access_token")
    return None

def home(request):
    uuid = None
    access_token = None
    refresh_token = None
    group_token = None
    if request.user.is_authenticated:
        uuid = request.user.social_auth.get(provider="globus").uid
        social = request.user.social_auth
        access_token = social.get(provider="globus").extra_data["access_token"]
        other_tokens = social.get(provider="globus").extra_data["other_tokens"]
        group_token = get_token(other_tokens, "urn:globus:auth:scope:nexus.api.globus.org:groups")
        refresh_token = social.get(provider="globus").extra_data["refresh_token"]
    return render(request,
                  "home.html",
                  {'uuid': uuid,
                  "access_token": access_token,
                  "refresh_token": refresh_token,
                  "group_token": group_token}
            )
