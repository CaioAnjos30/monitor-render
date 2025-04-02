import os
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"  # ID da planilha no Drive
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

def enviar_telegram(msg):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": msg}
        requests.post(url, data=data)
        print("📨 Mensagem enviada com sucesso.")
    else:
        print("❌ Variáveis do Telegram não configuradas.")

def get_modified_time():
    if not GOOGLE_CREDENTIALS:
        enviar_telegram("❌ GOOGLE_CREDENTIALS não encontrada.")
        return None

    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
    )

    service = build("drive", "v3", credentials=creds)
    file = service.files().get(fileId=FILE_ID, fields="modifiedTime").execute()
    modified_time = file["modifiedTime"]

    # Converter horário UTC para horário de Brasília
    dt = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
    dt_brasil = dt.astimezone(timezone(timedelta(hours=-3)))
    return dt_brasil.strftime("%d/%m/%Y %H:%M:%S")
