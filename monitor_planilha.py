# monitor_planilha.py

import os
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# CONFIGS
ID_ARQUIVO = '1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT'
CAMINHO_CREDENCIAL = 'credenciais_google.json'
ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'
TOKEN = '7498773442:AAEO8ihxIP18JtFSrO_6UGeC8VPtIJVH2rU'
CHAT_ID = '8142521159'

def get_modified_time():
    scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    creds = service_account.Credentials.from_service_account_file(CAMINHO_CREDENCIAL, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)
    file = service.files().get(fileId=ID_ARQUIVO, fields='modifiedTime').execute()
    return file['modifiedTime']

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    resposta = requests.post(url, data={'chat_id': CHAT_ID, 'text': mensagem})
    print("✅ Telegram enviado!" if resposta.status_code == 200 else f"❌ Erro: {resposta.text}")
