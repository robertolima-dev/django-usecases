from rest_framework import serializers

from apps.sheet_manager.models import SheetSanitizedData


class SheetSanitizedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetSanitizedData
        fields = [
            'id',
            'manager_sheet',
            'type_data',
            'sheet_line',
            'dt_created',
            'dt_updated',
            'dt_deleted',
        ]
        read_only_fields = ['id', 'dt_created', 'dt_updated', 'dt_deleted']
