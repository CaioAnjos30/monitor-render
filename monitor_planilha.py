import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

ID_ARQUIVO = '1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT'  # <-- Coloque o ID do seu arquivo
ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'
TOKEN = '7498773442:AAEO8ihxIP18JtFSrO_6UGeC8VPtIJVH2rU'
CHAT_ID = '8142521159'

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    resposta = requests.post(url, data={'chat_id': CHAT_ID, 'text': mensagem})
    if resposta.status_code == 200:
        print("✅ Telegram enviado!")
    else:
        print(f"❌ Falha ao enviar: {resposta.text}")

def get_ultima_atividade():
    google_creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not google_creds_json:
        raise ValueError("❌ Variável de ambiente GOOGLE_CREDENTIALS não encontrada!")

    cred_dict = json.loads(google_creds_json)
    scopes = ['https://www.googleapis.com/auth/drive.activity.readonly']
    creds = service_account.Credentials.from_service_account_info(cred_dict, scopes=scopes)
    service = build('driveactivity', 'v2', credentials=creds)

    body = {
        "itemName": f"items/{ID_ARQUIVO}",
        "pageSize": 1
    }

    response = service.activity().query(body=body).execute()
    atividades = response.get('activities', [])

    if not atividades:
        raise ValueError("❌ Nenhuma atividade encontrada para o arquivo.")

    atividade = atividades[0]
    user = atividade['actors'][0].get('user', {}).get('knownUser', {}).get('personName', 'Desconhecido')
    email = atividade['actors'][0].get('user', {}).get('knownUser', {}).get('personName', 'sem email')

    timestamp = atividade.get('timestamp')
    if not timestamp:
        timestamp = atividade['timeRange']['endTime']

    return timestamp, email



def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    resposta = requests.post(url, data={'chat_id': CHAT_ID, 'text': mensagem})
    print("✅ Telegram enviado!" if resposta.status_code == 200 else f"❌ Erro: {resposta.text}")
