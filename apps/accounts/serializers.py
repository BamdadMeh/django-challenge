from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import (

    ModelSerializer,
    CharField,
    ValidationError,
)

User = get_user_model()


class UserSerializer(ModelSerializer):

    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

        extra_kwargs = {
            'password': {'write_only': True},
            }

    def validate(self, data):

        if data['password'] != data['confirm_password']:
            raise ValidationError(_('The two password fields didn’t match.'))
        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)
