from rest_framework_simplejwt.backends import TokenBackend
from django.core.exceptions import ValidationError
import logging


logger = logging.getLogger('LMS')


class SetJWTUserMiddleware:

    """
        Middleware to set the user
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not (request.path.startswith('/api/token') or
                request.path.startswith('/api/register/')):
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            data = {'token': token}
            try:
                valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
                user_id = valid_data['user_id']
                request.user_id = user_id
            except ValidationError as v:
                logger.error("Error occured during decoding"+str(v))
        
        response = self.get_response(request)
        return response