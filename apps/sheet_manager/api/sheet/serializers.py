from rest_framework import serializers

from apps.sheet_manager.models import ManagerSheet


class ManagerSheetSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    file_exists = serializers.SerializerMethodField()
    
    class Meta:
        model = ManagerSheet
        fields = [
            'id',
            'user',
            'file',
            'file_name',
            'file_url',
            'file_exists',
            'formatter',
            'table_html',
            'type_of_data',
            'created_at',
            'updated_at',
            'deleted_at',
        ]
        read_only_fields = ['id', 'user', 'file_name', 'file_url', 'file_exists', 'created_at', 'updated_at', 'deleted_at']

    def get_file_name(self, obj):
        return obj.get_file_name()

    def get_file_url(self, obj):
        return obj.get_file_url()

    def get_file_exists(self, obj):
        return obj.file_exists()


class ManagerSheetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerSheet
        fields = ['file', 'type_of_data']
        
    def validate_file(self, value):
        if not value:
            raise serializers.ValidationError("O arquivo é obrigatório.")
        
        if not value.name:
            raise serializers.ValidationError("O arquivo deve ter um nome válido.")
        
        # Verificar extensão do arquivo
        allowed_extensions = ['.xlsx', '.xls', '.csv']
        file_extension = value.name.lower()
        if not any(file_extension.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                f"Formato de arquivo não suportado. Use: {', '.join(allowed_extensions)}"
            )
        
        return value
