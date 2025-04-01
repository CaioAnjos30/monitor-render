from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
ARQUIVO_ID = '1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT'  # ID da sua planilha

def descobrir_quem_e_quem():
    if not GOOGLE_CREDENTIALS:
        raise Exception("❌ GOOGLE_CREDENTIALS não definida.")

    info = json.loads(GOOGLE_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_info(info, scopes=[
        'https://www.googleapis.com/auth/drive'
    ])

    service = build('drive', 'v3', credentials=creds)

    resultado = service.permissions().list(
        fileId=ARQUIVO_ID,
        fields="permissions(id,emailAddress,displayName)"
    ).execute()

    permissoes = resultado.get('permissions', [])

    print("🔍 Mapeamento de usuários com acesso:")
    for p in permissoes:
        pid = f"people/{p['id']}"
        nome = p.get("displayName", "sem nome")
        email = p.get("emailAddress", "sem email")
        print(f'{pid}: {nome} ({email})')

if __name__ == "__main__":
    descobrir_quem_e_quem()
