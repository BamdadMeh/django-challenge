from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (

    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.accounts.serializers import UserSerializer
from apps.accounts.permissions import IsAnonymous


class UserCreateAPIView(APIView):
    """
    Create a new user.
    Permission : Only anonymous users have access.
    """

    serializer_class = UserSerializer
    permission_classes = (IsAnonymous,)

    def post(self, request):

        srz_data = self.serializer_class(data=request.data)

        if srz_data.is_valid():

            srz_data.create(srz_data.validated_data)
            return Response(data=srz_data.data, status=HTTP_201_CREATED)

        return Response(data=srz_data.errors, status=HTTP_400_BAD_REQUEST)


class UserLoginAPIView(TokenObtainPairView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAnonymous,)


class UserTokenRefreshView(TokenRefreshView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)


class UserTokenVerifyView(TokenVerifyView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
