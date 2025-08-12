from django.core.management.base import BaseCommand
from apps.sheet_manager.models import ManagerSheet


class Command(BaseCommand):
    help = 'Limpa objetos ManagerSheet com arquivos corrompidos ou ausentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra o que seria deletado sem realmente deletar',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: Nenhum objeto será deletado'))
        
        corrigidos = 0
        deletados = 0
        
        for ms in ManagerSheet.objects.all():
            # Se o campo file está vazio ou nulo
            if not ms.file or not ms.file.name:
                if dry_run:
                    self.stdout.write(f"DRY-RUN: ManagerSheet ID {ms.id} seria deletado (file vazio/nulo)")
                else:
                    self.stdout.write(f"Deletando ManagerSheet ID {ms.id} (file vazio/nulo)")
                    ms.delete()
                deletados += 1
                continue

            # Tenta acessar a URL do arquivo (verifica se existe no storage)
            try:
                _ = ms.file.url  # Isso vai dar erro se o arquivo não existir no S3/local
            except Exception as e:
                if dry_run:
                    self.stdout.write(f"DRY-RUN: ManagerSheet ID {ms.id} seria deletado (file inválido: {ms.file.name})")
                else:
                    self.stdout.write(f"Deletando ManagerSheet ID {ms.id} (file inválido: {ms.file.name})")
                    ms.delete()
                deletados += 1

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'DRY-RUN: {deletados} objetos seriam deletados')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Total corrigidos: {corrigidos}, Total deletados: {deletados}')
            ) 