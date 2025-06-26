from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integrations.api.serializers import OpenAITestSerializer
from apps.integrations.http_client import HTTPClient
from apps.integrations.openai_client import OpenAIClient


class OpenAITestView(APIView):
    def post(self, request):
        serializer = OpenAITestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = OpenAIClient(simulate_failure=serializer.validated_data["simulate_failure"])  # noqa: E501
        try:
            result = client.call_chat_completion([
                {"role": "user", "content": serializer.validated_data["message"]}  # noqa: E501
            ])
            return Response({"response": result})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # noqa: E501


class TestHttpClientView(APIView):
    def post(self, request):
        urls = request.data.get("urls", [])
        if not urls or not isinstance(urls, list):
            return Response({"error": "Envie uma lista de URLs no campo 'urls'"}, status=status.HTTP_400_BAD_REQUEST)  # noqa: E501

        client = HTTPClient()
        results = []

        headers = {
            "Authorization": "Bearer seu_token_aqui",
            "Content-Type": "application/json"
        }
        payload = {"title": "foo", "body": "bar", "userId": 1}

        if request.data.get("method", 'get') == 'get':
            for url in urls:
                result = client.get(url)
                results.append({"url": url, "response": result})

            return Response(results, status=status.HTTP_200_OK)

        elif request.data.get("method", None) == 'post':
            for url in urls:
                result = client.post(url, json=payload, headers=headers)
                results.append({"url": url, "response": result})

            return Response(results, status=status.HTTP_200_OK)
