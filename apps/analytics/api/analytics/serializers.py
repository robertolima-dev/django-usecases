from rest_framework import serializers


class EventLogSerializer(serializers.Serializer):
    event_type = serializers.CharField(max_length=50)
    description = serializers.CharField()
    timestamp = serializers.DateTimeField()
