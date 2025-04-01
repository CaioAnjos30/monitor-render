from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import pytz
import os
import json
import requests

# 📂 Variável de ambiente com as credenciais Google
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')

# ✅ ID do arquivo XLSX no Google Drive
ARQUIVO_ID = '1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT'

# ✅ Token e chat ID do bot Telegram
TELEGRAM_TOKEN = '7498773442:AAEO8ihxIP18JtFSrO_6UGeC8VPtIJVH2rU'
TELEGRAM_CHAT_ID = '8142521159'

def get_ultima_atividade():
    if not GOOGLE_CREDENTIALS:
        raise Exception("❌ Variável de ambiente GOOGLE_CREDENTIALS não encontrada!")

    info = json.loads(GOOGLE_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_info(info, scopes=[
        'https://www.googleapis.com/auth/drive.activity.readonly'
    ])

    service = build('driveactivity', 'v2', credentials=creds)

    body = {
        "itemName": f"items/{ARQUIVO_ID}",
        "pageSize": 1
    }

    response = service.activity().query(body=body).execute()
    activities = response.get("activities", [])

    if not activities:
        raise Exception("⚠️ Nenhuma atividade encontrada para o arquivo.")

    atividade = activities[0]
    atores = atividade.get("actors", [])

    # ⏰ Converte horário UTC para Brasil
    horario_utc = atividade.get("timestamp")
    horario_dt = datetime.strptime(horario_utc, "%Y-%m-%dT%H:%M:%S.%fZ")
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    horario_brasil = horario_dt.replace(tzinfo=pytz.utc).astimezone(fuso_brasil)
    horario_formatado = horario_brasil.strftime("%d/%m/%Y %H:%M:%S")

    # 👤 Tenta pegar o nome do usuário
    nome = "Desconhecido"
    for ator in atores:
        user = ator.get("user", {})
        known_user = user.get("knownUser", {})
        if known_user:
            nome = known_user.get("displayName", "Desconhecido")
            break

    return horario_formatado, nome

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    response = requests.post(url, data={
        'chat_id': TELEGRAM_CHAT_ID,
        'text': mensagem
    })

    if response.status_code == 200:
        print("✅ Mensagem enviada ao Telegram!")
    else:
        print(f"❌ Erro ao enviar mensagem: {response.text}")
