#!/usr/bin/env python
"""
Script simples para testar o upload
"""
import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_core.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from apps.sheet_manager.models import ManagerSheet

def test_simple_upload():
    """Testa o upload de forma simples"""
    print("=== Teste Simples de Upload ===")
    
    try:
        # Pegar um usuário
        user = User.objects.first()
        if not user:
            print("❌ Nenhum usuário encontrado")
            return
        
        print(f"✅ Usando usuário: {user.email}")
        
        # Criar um arquivo de teste
        test_content = "Teste de planilha simples"
        content_file = ContentFile(test_content.encode('utf-8'), name="test_simple.xlsx")
        
        # Criar o ManagerSheet
        manager_sheet = ManagerSheet.objects.create(
            user=user,
            file=content_file,
            type_of_data='financial_data'
        )
        
        print(f"✅ ManagerSheet criado com sucesso!")
        print(f"   - ID: {manager_sheet.id}")
        print(f"   - File name: {manager_sheet.get_file_name()}")
        print(f"   - File exists: {manager_sheet.file_exists()}")
        print(f"   - Created at: {manager_sheet.created_at}")
        
        # Testar o serializer
        from apps.sheet_manager.api.sheet.serializers import ManagerSheetSerializer
        serializer = ManagerSheetSerializer(manager_sheet)
        print(f"✅ Serializer funcionando: {serializer.data['id']}")
        
        # Deletar o objeto de teste
        manager_sheet.delete()
        print("✅ Objeto de teste deletado")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_upload() 