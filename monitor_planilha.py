import os
import json
import requests
from datetime import datetime, timedelta, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ID da planilha .xlsx no Google Drive
ID_ARQUIVO = '1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT'
ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'

# Telegram
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

    # Tenta pegar e-mail do usuário
    usuario = atividade['actors'][0].get('user', {}).get('knownUser', {}).get('emailAddress')
    if not usuario:
        usuario = 'Desconhecido'

    # Pega o horário e converte de UTC para GMT-3
    timestamp = atividade.get('timestamp') or atividade['timeRange']['endTime']
    horario_utc = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    horario_br = horario_utc.astimezone(timezone(timedelta(hours=-3)))
    horario_formatado = horario_br.strftime("%d/%m/%Y %H:%M:%S")

    return horario_formatado, usuario
