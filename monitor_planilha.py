import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# === Configurações ===
ID_ARQUIVO = '1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT'
ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'
TOKEN = '7498773442:AAEO8ihxIP18JtFSrO_6UGeC8VPtIJVH2rU'
CHAT_ID = '8142521159'

def get_modified_time():
    # Lê credencial da variável de ambiente
    google_creds_json = os.environ.get('GOOGLE_CREDENTIALS')

    if not google_creds_json:
        raise ValueError("❌ Variável de ambiente GOOGLE_CREDENTIALS não encontrada!")

    # Converte string JSON para dicionário
    cred_dict = json.loads(google_creds_json)

    scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    creds = service_account.Credentials.from_service_account_info(cred_dict, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)

    file = service.files().get(fileId=ID_ARQUIVO, fields='modifiedTime').execute()
    return file['modifiedTime']

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    resposta = requests.post(url, data={'chat_id': CHAT_ID, 'text': mensagem})
    print("✅ Telegram enviado!" if resposta.status_code == 200 else f"❌ Erro: {resposta.text}")

