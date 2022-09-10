from django.contrib.auth.forms import (
     UserCreationForm as BaseUserCreationForm,
     UserChangeForm as BaseUserChangeForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(BaseUserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
