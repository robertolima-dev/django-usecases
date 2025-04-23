from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.users.managers.profile_manager import ProfileManager

from .serializers import ProfileSerializer


@extend_schema(
    tags=["Profile"]
)
class ProfileApiView(APIView):
    serializer_class = ProfileSerializer
    http_method_names = ['post', 'patch', ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        profile_serializer = ProfileSerializer(data=request.data)
        if not profile_serializer.is_valid():
            return Response(profile_serializer.errors, status=HTTP_400_BAD_REQUEST) # noqa501

        try:

            manager = ProfileManager()
            manager.create_or_update_profile(
                user=request.user,
                profile_serializer=profile_serializer
            )

            return Response({
                'profile': profile_serializer.data
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )

    def patch(self, request, ):

        try:

            manager = ProfileManager()
            instance = manager.change_access_level(
                user=request.user
            )

            serializer = ProfileSerializer(data=[instance], many=True)
            serializer.is_valid()

            return Response(
                serializer.data[0],
                status=HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )


@extend_schema(
    tags=["Profile"]
)
class ProfileDataApiView(APIView):
    serializer_class = ProfileSerializer
    http_method_names = ['get', ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):

        try:

            manager = ProfileManager()
            data = manager.get_profile_data(
                user=request.user
            )

            return Response(
                data,
                status=HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
                )
