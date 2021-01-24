from rest_framework import serializers
from django.conf import settings
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from ..models import LmsUser


class LmsUserSerializer(serializers.ModelSerializer):

    """
        FormSets serializer
    """

    class Meta:
        model = LmsUser
        fields = '__all__'

    def create(self, validated_data):
        return LmsUser.objects.create_user(**validated_data)

    def validate(self, data):

        # get the password from the data
        password = data.get('password')
        role = data.get('role')

        errors = dict()
        # validate the password and catch the exception
        try:
            validators.validate_password(
                password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        if role and role.is_digit() and int(role) == 2:
            raise serializers.ValidationError("Please contact admin to create Mentor")

        return super(LmsUserSerializer, self).validate(data)
