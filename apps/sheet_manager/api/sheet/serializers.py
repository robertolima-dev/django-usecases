from rest_framework import serializers

from apps.sheet_manager.models import ManagerSheet


class ManagerSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerSheet
        fields = [
            'id',
            'user',
            'file',
            'formatter',
            'table_html',
            'type_of_data',
            'dt_created',
            'dt_updated',
            'dt_deleted',
        ]
        read_only_fields = ['id', 'user', 'dt_created', 'dt_updated', 'dt_deleted']  # noqa: E501
