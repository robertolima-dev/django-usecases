import os

import boto3
import botocore
from django.conf import settings
from django.utils import timezone
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView


class FileUploadApiView(APIView):
    parser_classes = (MultiPartParser,)
    http_method_names = ['post', ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, ):

        AWS_BUCKET = settings.AWS_BUCKET
        AWS_S3_LINK = settings.AWS_S3_LINK

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
            )

        file = request.FILES['file']
        if file:

            try:

                file_name, file_extension = os.path.splitext(file.name)

                hash_name = hash(file.name + str(timezone.now()))
                new_file_name_hashed = str(hash_name) + file_extension
                new_file_name = new_file_name_hashed.replace('-', '')

                s3.upload_fileobj(file.file, AWS_BUCKET, new_file_name)

                link = AWS_S3_LINK + '/' + new_file_name
                return Response(
                    {"link": link},
                    status=HTTP_201_CREATED
                    )

            except botocore.exceptions.ClientError as e:
                return Response(
                    {'detail': str(e)},
                    status=HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                status=HTTP_406_NOT_ACCEPTABLE
            )
