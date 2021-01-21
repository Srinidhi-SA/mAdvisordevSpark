from api.models.profile import Profile
from rest_framework.exceptions import AuthenticationFailed


def get_current_user(request):

    token = request.META.get('HTTP_TOKEN') or request.META.get('HTTP_X_TOKEN')
    if not token:
        raise AuthenticationFailed(detail="Please provied a User Token")
    try:
        profile = Profile.objects.get(token=token)
        return profile.user
    except Profile.DoesNotExist as e:
        raise AuthenticationFailed(detail="Invalid user token provided. Please provide a active user token.")