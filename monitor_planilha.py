import os
import json
import requests
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytz

# 🚨 Token e Chat ID do seu Bot Telegram
TOKEN = '7498773442:AAEO8ihxIP18JtFSrO_6UGeC8VPtIJVH2rU'
CHAT_ID = '8142521159'

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    resposta = requests.post(url, data={
        'chat_id': CHAT_ID,
        'text': mensagem
    })
    if resposta.status_code == 200:
        print("✅ Mensagem enviada via Telegram!")
    else:
        print(f"❌ Falha ao enviar mensagem: {resposta.text}")

def get_ultima_atividade():
    SCOPES = ['https://www.googleapis.com/auth/drive.activity.readonly']
    ARQUIVO_CRED = os.environ.get('GOOGLE_CREDENTIALS')

    if not ARQUIVO_CRED:
        raise Exception("❌ Variável de ambiente GOOGLE_CREDENTIALS não encontrada!")

    creds = service_account.Credentials.from_service_account_info(
        json.loads(ARQUIVO_CRED), scopes=SCOPES)
    service = build('driveactivity', 'v2', credentials=creds)

    response = service.activity().query(body={
        "pageSize": 1,
        "filter": "detail.action_detail_case:EDIT"
    }).execute()

    activities = response.get('activities', [])
    if not activities:
        raise Exception("❌ Nenhuma atividade recente encontrada.")

    time_str = activities[0]['timestamp']
    horario = datetime.fromisoformat(time_str.replace("Z", "+00:00")).astimezone(
        pytz.timezone("America/Sao_Paulo"))
    horario_str = horario.strftime("%d/%m/%Y %H:%M:%S")

    nome = "Desconhecido"
    atores = activities[0].get("actors", [])
    for ator in atores:
        user = ator.get("user", {})
        known_user = user.get("knownUser", {})
        if known_user:
            nome = known_user.get("displayName", "Desconhecido")
            if nome != "Desconhecido":
                break

    return horario_str, nome
