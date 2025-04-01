import os
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

# === CONFIGURAÇÕES ===
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"
ARQUIVO_MODIFICACAO = "ultima_modificacao.txt"


def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Variáveis do Telegram não configuradas.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensagem})
    if response.status_code == 200:
        print("📨 Mensagem enviada com sucesso.")
    else:
        print(f"❌ Erro ao enviar mensagem: {response.text}")


def get_modified_time():
    creds = service_account.Credentials.from_service_account_info(
        json.loads(GOOGLE_CREDENTIALS),
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
    )
    service = build("drive", "v3", credentials=creds)
    file = service.files().get(fileId=FILE_ID, fields="modifiedTime").execute()

    modified_time = file["modifiedTime"]
    dt = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
    dt_brasil = dt.astimezone(timezone(timedelta(hours=-3)))
    return dt_brasil.strftime("%d/%m/%Y %H:%M:%S")


def main():
    nova_data = get_modified_time()
    if not nova_data:
        print("❌ Não foi possível obter data.")
        return

    data_antiga = ""
    if os.path.exists(ARQUIVO_MODIFICACAO):
        with open(ARQUIVO_MODIFICACAO, "r") as f:
            data_antiga = f.read().strip()

    if nova_data != data_antiga:
        mensagem = f"📢 A planilha foi modificada!\n🕒 Quando: {nova_data}"
        enviar_telegram(mensagem)
        with open(ARQUIVO_MODIFICACAO, "w") as f:
            f.write(nova_data)
        print("✅ Modificação detectada e alerta enviado.")
    else:
        print("🟢 Nenhuma nova modificação.")


if __name__ == "__main__":
    main()
