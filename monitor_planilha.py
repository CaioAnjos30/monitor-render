import os
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

# ID do ARQUIVO .xlsx (não Google Sheets!)
FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"

# Variável de ambiente com JSON das credenciais
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

def enviar_telegram(msg):
    """Envia mensagem no Telegram via bot."""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("❌ Variáveis do Telegram não configuradas.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": msg}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("📨 Mensagem enviada com sucesso.")
        else:
            print(f"❌ Erro ao enviar mensagem: {response.text}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem Telegram: {e}")

def get_modified_time():
    """Retorna a data da última modificação do arquivo no formato BR (UTC-3)."""
    if not GOOGLE_CREDENTIALS:
        print("❌ GOOGLE_CREDENTIALS não encontrada.")
        return None

    try:
        creds_dict = json.loads(GOOGLE_CREDENTIALS)
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
        )

        service = build("drive", "v3", credentials=creds)
        file = service.files().get(
            fileId=FILE_ID,
            fields="modifiedTime"
        ).execute()

        modified_time = file["modifiedTime"]

        # Converter UTC para horário de Brasília
        dt = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
        dt_brasil = dt.astimezone(timezone(timedelta(hours=-3)))
        return dt_brasil.strftime("%d/%m/%Y %H:%M:%S")

    except Exception as e:
        print(f"❌ Erro ao obter modificação: {e}")
        return None

# Teste local
if __name__ == "__main__":
    data = get_modified_time()
    if data:
        print(f"🕒 Última modificação: {data}")
        enviar_telegram(f"🔍 Última modificação detectada: {data}")
    else:
        print("⚠️ Nenhuma modificação encontrada.")
