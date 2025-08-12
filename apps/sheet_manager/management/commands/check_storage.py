from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Verifica as configurações do storage'

    def handle(self, *args, **options):
        self.stdout.write("=== Verificação do Storage ===")
        
        # Verificar configurações
        self.stdout.write(f"PROJECT_ENV: {getattr(settings, 'PROJECT_ENV', 'Não definido')}")
        self.stdout.write(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Não definido')}")
        self.stdout.write(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'Não definido')}")
        self.stdout.write(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Não definido')}")
        
        # Verificar se o storage está funcionando
        try:
            storage = default_storage
            self.stdout.write(f"Storage class: {storage.__class__.__name__}")
            
            # Testar operações básicas
            test_file = "test_storage.txt"
            test_content = "Teste de storage"
            
            # Criar ContentFile corretamente
            content_file = ContentFile(test_content.encode('utf-8'))
            
            # Salvar arquivo
            file_path = storage.save(test_file, content_file)
            self.stdout.write("✅ Arquivo salvo com sucesso")
            
            # Verificar se existe
            if storage.exists(file_path):
                self.stdout.write("✅ Arquivo existe")
            else:
                self.stdout.write("❌ Arquivo não existe")
            
            # Deletar arquivo
            storage.delete(file_path)
            self.stdout.write("✅ Arquivo deletado com sucesso")
            
        except Exception as e:
            self.stdout.write(f"❌ Erro no storage: {e}")
            import traceback
            traceback.print_exc()
        
        # Verificar configurações do S3 se aplicável
        if 's3' in getattr(settings, 'DEFAULT_FILE_STORAGE', '').lower():
            self.stdout.write("\n=== Configurações S3 ===")
            self.stdout.write(f"AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Não definido')}")
            self.stdout.write(f"AWS_ACCESS_KEY_ID: {'Definido' if getattr(settings, 'AWS_ACCESS_KEY_ID', None) else 'Não definido'}")
            self.stdout.write(f"AWS_SECRET_ACCESS_KEY: {'Definido' if getattr(settings, 'AWS_SECRET_ACCESS_KEY', None) else 'Não definido'}")
            self.stdout.write(f"AWS_S3_REGION_NAME: {getattr(settings, 'AWS_S3_REGION_NAME', 'Não definido')}")
        
        self.stdout.write("\n✅ Verificação concluída!") 