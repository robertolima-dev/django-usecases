from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView

from apps.users.managers.user_manage import UserDataManager

from .authentication import expires_in
from .serializers import (
    ChangePasswordSerializer,
    ConfirmEmailSerializer,
    CreateUserSerializer,
    ForgorPasswordSerializer,
    UnsubscribeSerializer,
    UserSerializer,
    UserSigninSerializer,
)


@extend_schema(
    tags=["Auth"]
)
class AuthenticationApiView(APIView):
    serializer_class = UserSigninSerializer
    http_method_names = ['post', ]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        signin_serializer = UserSigninSerializer(data=request.data)
        signin_serializer.is_valid(raise_exception=True)

        try:

            manager = UserDataManager()
            data, _ = manager.auth_user(signin_serializer)

            return Response(
                data,
                status=HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )


@extend_schema(
    tags=["Auth"]
)
class UserInfoApiView(APIView):
    serializer_class = UserSigninSerializer
    http_method_names = ['get', ]

    def get(self, request):

        try:

            user_serialized = UserSerializer(request.user)

            return Response({
                'user': user_serialized.data,
                'expires_in': expires_in(request.auth),
                'token': request.auth.key
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )


@extend_schema(
    tags=["Auth"]
)
class CreateUserView(APIView):
    serializer_class = UserSigninSerializer
    http_method_names = ['post', ]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        register_serializer = CreateUserSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)

        try:

            manager = UserDataManager()
            data, _ = manager.register_user(request=request)

            return Response(
                data,
                status=HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )


@extend_schema(
    tags=["Auth"]
)
class ConfirmEmailView(APIView):
    serializer_class = ConfirmEmailSerializer
    http_method_names = ['post', ]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        confirm_email_serializer = ConfirmEmailSerializer(data=request.data)

        if not confirm_email_serializer.is_valid():
            return Response(
                confirm_email_serializer.errors,
                status=HTTP_400_BAD_REQUEST
                )

        try:

            manager = UserDataManager()
            manager.confirm_email_user(
                hash=confirm_email_serializer.data['hash']
                )

            return Response(
                {'message': 'Email confirmado com sucesso'},
                status=HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )


@extend_schema(
    tags=["Auth"]
)
class ForgotPasswordView(APIView):
    serializer_class = ForgorPasswordSerializer
    http_method_names = ['post', ]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        forgot_password_serializer = ForgorPasswordSerializer(data=request.data) # noqa501

        if not forgot_password_serializer.is_valid():
            return Response(
                forgot_password_serializer.errors,
                status=HTTP_400_BAD_REQUEST
                )

        try:

            email = forgot_password_serializer.data['email'].lower().strip()

            manager = UserDataManager()
            manager.forgot_password_user(
                email=email
                )

            return Response(
                {'message': 'Email enviado para troca de senha'},
                status=HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_404_NOT_FOUND
                )


@extend_schema(
    tags=["Auth"]
)
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    http_method_names = ['post', ]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        change_password_serializer = ChangePasswordSerializer(data=request.data) # noqa501

        if not change_password_serializer.is_valid():
            return Response(
                change_password_serializer.errors,
                status=HTTP_400_BAD_REQUEST
                )

        try:

            manager = UserDataManager()
            data, _ = manager.change_password_user(
                hash=change_password_serializer.data.get('hash', None),
                jwt=change_password_serializer.data.get('jwt', None),
                new_password=change_password_serializer.data['password']
                )

            return Response(data, status=HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )


@extend_schema(
    tags=["Auth"]
)
class UserDeleteApiView(APIView):
    http_method_names = ['delete', ]
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, user_id, ):

        try:

            if user_id != request.user.id:
                return Response(
                    {'detail': 'Sem autorização'},
                    status=HTTP_401_UNAUTHORIZED
                    )

            manager = UserDataManager()
            manager.delete_user(
                user=request.user
            )

            return Response(
                status=HTTP_204_NO_CONTENT
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )


@extend_schema(
    tags=["Auth"]
)
class MfaApiView(APIView):
    serializer_class = UserSigninSerializer
    http_method_names = ['post', ]
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        return Response(
            {'detail': 'disabled'},
            status=HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Auth"]
)
class UnsubscribeApiView(APIView):
    serializer_class = UnsubscribeSerializer
    http_method_names = ['post', ]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        unsubscribe_serializer = UnsubscribeSerializer(data=request.data)

        if not unsubscribe_serializer.is_valid():
            return Response(
                unsubscribe_serializer.errors,
                status=HTTP_400_BAD_REQUEST
                )

        try:

            manager = UserDataManager()
            manager.unsubscribe_user(
                hash=unsubscribe_serializer.data['hash'],
                unsubscribe=unsubscribe_serializer.data['unsubscribe']
                )

            return Response(
                {'message': 'Unsubscribe confirmed successfully'},
                status=HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )
