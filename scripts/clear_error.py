

class ClearError:

    def run(self):
        from apps.sheet_manager.models import ManagerSheet

        corrigidos = 0
        deletados = 0
        for ms in ManagerSheet.objects.all():
            # Se o campo file está vazio ou nulo
            if not ms.file or not ms.file.name:
                print(f"ManagerSheet ID {ms.id} com file vazio/nulo. Deletando...")
                ms.delete()
                deletados += 1
                continue

            # Tenta acessar a URL do arquivo (verifica se existe no storage)
            try:
                _ = ms.file.url  # Isso vai dar erro se o arquivo não existir no S3/local
            except Exception as e:
                print(f"ManagerSheet ID {ms.id} com file inválido ({ms.file.name}): {e}. Deletando...")
                ms.delete()
                deletados += 1

        print(f"Total corrigidos: {corrigidos}, Total deletados: {deletados}")