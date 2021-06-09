from __future__ import print_function
# from auditlog.middleware import AuditlogMiddleware
#
#
#
# class ModifiedAuditlogMiddleware(AuditlogMiddleware):
#     def process_request(self, request):
#         """
#         Gets the current user from the request and prepares and connects a signal receiver with the user already
#         attached to it.
#         """
#         # Initialize thread local storage
#         threadlocal.auditlog = {
#             'signal_duid': (self.__class__, time.time()),
#             'remote_addr': request.META.get('REMOTE_ADDR'),
#         }
#
#         # In case of proxy, set 'original' address
#         if request.META.get('HTTP_X_FORWARDED_FOR'):
#             threadlocal.auditlog['remote_addr'] = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
#
#         # Connect signal for automatic logging
#
#         if hasattr(request, 'user') and hasattr(request.user, 'is_authenticated') and request.user.is_authenticated():
#             set_actor = curry(self.set_actor, user=request.user, signal_duid=threadlocal.auditlog['signal_duid'])
#             pre_save.connect(set_actor, sender=LogEntry, dispatch_uid=threadlocal.auditlog['signal_duid'], weak=False)


# from rest_framework.request import Request
# from django.utils.functional import SimpleLazyObject
# from django.contrib.auth.middleware import get_user
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#
# def get_user_jwt(request):
#     user = get_user(request)
#     if user.is_authenticated():
#         return user
#     try:
#         user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
#         if user_jwt is not None:
#             return user_jwt[0]
#     except:
#         pass
#     return user
#
#
# class AuthenticationMiddlewareJWT(object):
#     def process_request(self, request):
#         assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
#
#         request.user = SimpleLazyObject(lambda: get_user_jwt(request))


from builtins import object
from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class AuthenticationMiddlewareJWT(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JSONWebTokenAuthentication()
        if jwt_authentication.get_jwt_value(request):
            jwt_value = jwt_authentication.get_jwt_value(request)
            import jwt
            try:
                payload = jwt_decode_handler(jwt_value)
            except jwt.ExpiredSignature:
                print("Signature expired.")
                msg = {
                    'jwtResponse': 'Signature has expired.'
                }
                return msg
            except jwt.DecodeError:
                print('Error decoding signature.')
                msg = {
                    'jwtResponse': 'Error decoding signature.'
                }
                return msg
            except jwt.InvalidTokenError:
                print("invalid token error")
                return exceptions.AuthenticationFailed()

            user = jwt_authentication.authenticate_credentials(payload)

            user, jwt = jwt_authentication.authenticate(request)
        return user

class PrintRequestMiddleware(object):
    """
    Provides full logging of requests and responses
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            print(request.META['HTTP_AUTHORIZATION'])
        return self.get_response(request)

#
# class JWTAuthMiddleware(object):
#     """
#     Convenience middleware for users of django-rest-framework-jwt.
#     Fixes issue https://github.com/GetBlimp/django-rest-framework-jwt/issues/45
#     """
#
#
#     def get_user_jwt(self, request):
#         from rest_framework.request import Request
#         from rest_framework.exceptions import AuthenticationFailed
#         from django.utils.functional import SimpleLazyObject
#         from django.contrib.auth.middleware import get_user
#         from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#
#         user = get_user(request)
#         if user.is_authenticated():
#             return user
#         try:
#             user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
#             if user_jwt is not None:
#                 return user_jwt[0]
#         except AuthenticationFailed:
#             pass
#         return user
#
#     def process_request(self, request):
#         from django.utils.functional import SimpleLazyObject
#         assert hasattr(request, 'session'),\
#         """The Django authentication middleware requires session middleware to be installed.
#          Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."""
#
#         request.user = SimpleLazyObject(lambda: self.get_user_jwt(request))
