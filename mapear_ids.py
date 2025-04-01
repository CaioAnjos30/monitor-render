from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# 🔐 Lê as credenciais do ambiente
creds_json = os.getenv("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# ✅ ID da sua pasta
ID_PASTA = '1FyYUWwcV2kr7flcUF9HbDgUB0AJXIyr9'

def listar_permissoes():
    print("🔍 Buscando permissões da PASTA...")
    resultados = service.permissions().list(
        fileId=ID_PASTA,
        fields="permissions(id,emailAddress,displayName)",
        supportsAllDrives=True
    ).execute()

    permissoes = resultados.get('permissions', [])

    if not permissoes:
        print("❌ Nenhuma permissão encontrada.")
        return

    print("\n✅ MAPA_PESSOAS = {\n")
    for perm in permissoes:
        pessoa_id = f"people/{perm['id']}"
        nome = perm.get('displayName', 'Sem nome')
        email = perm.get('emailAddress', 'Sem email')
        print(f'    "{pessoa_id}": "{nome} ({email})",')
    print("}\n")

if __name__ == "__main__":
    listar_permissoes()
