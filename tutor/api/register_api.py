from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from ..models import LmsUser
from .register_api_serializers import LmsUserSerializer


class RegisterUser(GenericAPIView):

    """
        Register a user to LMS system
    """

    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        return LmsUserSerializer

    def post(self, request):

        """
            API to register Register user
        """

        response = {}
        serializer = LmsUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            status_code = status.HTTP_201_CREATED
            response['message'] = 'User registered successfully'
            response.update(self.serialize_response(user))
            return Response(response, status=status_code)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def serialize_response(self, user):

        """
            Serialize response
        """

        return {'email': user.email}
