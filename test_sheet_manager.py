#!/usr/bin/env python
"""
Script de teste para o app sheet_manager
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_core.settings')
django.setup()

from apps.sheet_manager.models import ManagerSheet
from django.contrib.auth.models import User

def test_sheet_manager():
    """Testa as funcionalidades do sheet_manager"""
    print("=== Teste do Sheet Manager ===")
    
    # Verificar se há usuários
    users = User.objects.all()
    if not users.exists():
        print("❌ Nenhum usuário encontrado. Crie um usuário primeiro.")
        return
    
    user = users.first()
    print(f"✅ Usando usuário: {user.email}")
    
    # Verificar ManagerSheets existentes
    sheets = ManagerSheet.objects.all()
    print(f"📊 Total de ManagerSheets: {sheets.count()}")
    
    # Verificar arquivos corrompidos
    corrupted = 0
    for sheet in sheets:
        try:
            if sheet.file and sheet.file.name:
                _ = sheet.file.url
            else:
                corrupted += 1
        except Exception:
            corrupted += 1
    
    print(f"⚠️  ManagerSheets com problemas: {corrupted}")
    
    # Testar métodos do modelo
    if sheets.exists():
        sheet = sheets.first()
        print(f"\n📋 Testando métodos do modelo:")
        print(f"   - ID: {sheet.id}")
        print(f"   - User: {sheet.user.email if sheet.user else 'No user'}")
        print(f"   - File name: {sheet.get_file_name()}")
        print(f"   - File URL: {sheet.get_file_url()}")
        print(f"   - File exists: {sheet.file_exists()}")
        print(f"   - __str__: {sheet}")
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    test_sheet_manager() 