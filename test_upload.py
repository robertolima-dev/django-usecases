#!/usr/bin/env python
"""
Script para testar o upload de arquivos
"""
import os
import sys
import django
import requests
from io import BytesIO

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_core.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.sheet_manager.models import ManagerSheet

def test_storage():
    """Testa o storage diretamente"""
    print("=== Teste do Storage ===")
    
    try:
        # Criar um arquivo de teste
        test_content = "Teste de upload"
        content_file = ContentFile(test_content.encode('utf-8'))
        
        # Salvar usando o storage
        file_path = default_storage.save("test_upload.txt", content_file)
        print(f"✅ Arquivo salvo: {file_path}")
        
        # Verificar se existe
        if default_storage.exists(file_path):
            print("✅ Arquivo existe no storage")
        else:
            print("❌ Arquivo não existe no storage")
        
        # Deletar
        default_storage.delete(file_path)
        print("✅ Arquivo deletado")
        
    except Exception as e:
        print(f"❌ Erro no storage: {e}")
        import traceback
        traceback.print_exc()

def test_model_creation():
    """Testa a criação do modelo"""
    print("\n=== Teste de Criação do Modelo ===")
    
    try:
        # Pegar um usuário
        user = User.objects.first()
        if not user:
            print("❌ Nenhum usuário encontrado")
            return
        
        # Criar um arquivo de teste
        test_content = "Teste de planilha"
        content_file = ContentFile(test_content.encode('utf-8'), name="test_sheet.xlsx")
        
        # Criar o ManagerSheet
        manager_sheet = ManagerSheet.objects.create(
            user=user,
            file=content_file,
            type_of_data='financial_data'
        )
        
        print(f"✅ ManagerSheet criado: {manager_sheet}")
        print(f"   - ID: {manager_sheet.id}")
        print(f"   - File name: {manager_sheet.get_file_name()}")
        print(f"   - File exists: {manager_sheet.file_exists()}")
        
        # Deletar o objeto de teste
        manager_sheet.delete()
        print("✅ Objeto de teste deletado")
        
    except Exception as e:
        print(f"❌ Erro na criação do modelo: {e}")
        import traceback
        traceback.print_exc()

def test_api_upload():
    """Testa o upload via API"""
    print("\n=== Teste de Upload via API ===")
    
    try:
        # URL da API
        url = "http://localhost:8000/api/v1/upload-sheet/"
        
        # Criar um arquivo de teste
        test_content = "Teste de planilha via API"
        files = {
            'file': ('test_api.xlsx', test_content, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        # Headers (você precisa de um token válido)
        headers = {
            'Authorization': 'Token SEU_TOKEN_AQUI'  # Substitua pelo token real
        }
        
        # Fazer o request
        response = requests.post(url, files=files, headers=headers)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro no teste da API: {e}")

if __name__ == "__main__":
    test_storage()
    test_model_creation()
    # test_api_upload()  # Descomente se quiser testar a API 