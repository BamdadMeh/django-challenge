from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from apps.stadium.models import Stadium
from apps.stadium.serializers import StadiumSerializer


class StadiumCreateAPIView(CreateAPIView):
    """
    Create a new stadium.
    Permission : Only admin users have access.
    Accept the following POST parameters: name.
    Returns : StadiumModel fields or fail message.
    """

    permission_classes = (IsAdminUser,)

    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
