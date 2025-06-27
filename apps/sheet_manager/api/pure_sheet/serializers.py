from rest_framework import serializers

from apps.sheet_manager.models import SheetPureData


class SheetPureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetPureData
        fields = [
            'id',
            'manager_sheet',
            'type_data',
            'sheet_line',
            'sanitized',
            'dt_created',
            'dt_updated',
            'dt_deleted',
        ]
        read_only_fields = ['id', 'dt_created', 'dt_updated', 'dt_deleted']
