from rest_framework import serializers


class OpenAITestSerializer(serializers.Serializer):
    message = serializers.CharField()
    simulate_failure = serializers.BooleanField(default=False)
