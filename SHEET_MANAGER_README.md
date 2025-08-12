# Sheet Manager - Documentação

## Visão Geral

O app `sheet_manager` foi modificado para ser mais robusto e lidar melhor com arquivos ausentes ou corrompidos no S3. As principais melhorias incluem:

- Métodos seguros para acessar arquivos
- Validações robustas
- Tratamento de erros melhorado
- Admin interface aprimorada
- API endpoints organizados

## Funcionalidades

### 1. Modelo ManagerSheet

**Métodos seguros adicionados:**
- `get_file_name()`: Retorna o nome do arquivo de forma segura
- `get_file_url()`: Retorna a URL do arquivo de forma segura
- `file_exists()`: Verifica se o arquivo existe no storage
- `clean()`: Validação customizada do modelo

### 2. Admin Interface

**Melhorias:**
- Campo `file_status` que mostra se o arquivo existe ou não
- Método `file_name` seguro
- Tratamento de erros melhorado
- Interface mais informativa

### 3. API Endpoints

**Endpoints disponíveis:**
- `POST /api/v1/upload-sheet/`: Upload de planilhas
- `GET /api/v1/sheet-manager/sheets/`: Listar planilhas do usuário
- `GET /api/v1/sheet-manager/sheets/{id}/`: Detalhes de uma planilha
- `PUT /api/v1/sheet-manager/sheets/{id}/`: Atualizar planilha
- `DELETE /api/v1/sheet-manager/sheets/{id}/`: Deletar planilha

### 4. Comandos de Gerenciamento

**Comando para limpar objetos corrompidos:**
```bash
# Modo dry-run (apenas mostra o que seria deletado)
python manage.py clean_corrupted_sheets --dry-run

# Executar a limpeza
python manage.py clean_corrupted_sheets
```

## Como Usar

### 1. Limpar Objetos Corrompidos

Primeiro, execute o comando para limpar objetos com problemas:

```bash
python manage.py clean_corrupted_sheets --dry-run
```

Se o resultado parecer correto, execute sem o `--dry-run`:

```bash
python manage.py clean_corrupted_sheets
```

### 2. Testar o Sistema

Execute o script de teste:

```bash
python test_sheet_manager.py
```

### 3. Usar a API

**Upload de planilha:**
```bash
curl -X POST \
  -H "Authorization: Token SEU_TOKEN" \
  -F "file=@/caminho/para/planilha.xlsx" \
  -F "type_of_data=financial_data" \
  http://localhost:8000/api/v1/upload-sheet/
```

**Listar planilhas:**
```bash
curl -X GET \
  -H "Authorization: Token SEU_TOKEN" \
  http://localhost:8000/api/v1/sheet-manager/sheets/
```

### 4. Acessar o Admin

Acesse `http://localhost:8000/admin/sheet_manager/managersheet/` para ver:
- Lista de todas as planilhas
- Status dos arquivos (existe/não existe)
- Informações detalhadas

## Estrutura de Arquivos

```
apps/sheet_manager/
├── models.py                 # Modelo com métodos seguros
├── admin.py                  # Admin interface melhorada
├── api/
│   └── sheet/
│       ├── serializers.py    # Serializers com validações
│       └── viewsets.py       # Views e ViewSets
├── management/
│   └── commands/
│       └── clean_corrupted_sheets.py  # Comando de limpeza
└── urls.py                   # URLs do app
```

## Resolução de Problemas

### Erro "Required parameter name not set"

Este erro vem do boto3 (S3) quando um arquivo não existe mais no bucket. Para resolver:

1. Execute o comando de limpeza
2. Verifique se os objetos corrompidos foram removidos
3. Se o problema persistir, verifique as configurações do S3

### Arquivos não aparecem no admin

1. Verifique se o diretório `media/` existe
2. Verifique as permissões do diretório
3. Execute o script de teste para diagnosticar

### Upload não funciona

1. Verifique se o arquivo tem extensão válida (.xlsx, .xls, .csv)
2. Verifique se o arquivo tem um nome válido
3. Verifique as configurações de storage no `settings.py`

## Configurações Importantes

Certifique-se de que as seguintes configurações estão corretas no `settings.py`:

```python
# Para desenvolvimento local
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Para produção (S3)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_STATIC_FILES')
```

## Próximos Passos

1. Execute o comando de limpeza
2. Teste o upload de uma nova planilha
3. Verifique se o admin está funcionando
4. Teste os endpoints da API

Se ainda houver problemas, verifique os logs do Django para mais detalhes sobre os erros. 