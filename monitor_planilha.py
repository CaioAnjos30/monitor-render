import os
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Carrega credenciais
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

# ID do arquivo que será monitorado
FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"

# Mapa de pessoas conhecidas
MAPA_PESSOAS = {
    "people/00289363581191441115": "python-planilhas@black-moon-455013-a5.iam.gserviceaccount.com",
    "people/01708069321338839734": "Olívia Scanentech",
    "people/04174463028638780853": "Enzo Silva",
    "people/04296532891180382301": "Breno Mattos",
    "people/15062355278509587252": "Caio Anjos",
    "people/18141613163935753002": "Mtiemy (Scanntech)",
    "people/105257090019450438376": "Olívia Scanentech",
    "people/109989480159477284499": "Mtiemy (Scanntech)",
}

def enviar_telegram(mensagem):
    import requests
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    if not TOKEN or not CHAT_ID:
        print("❌ Variáveis do Telegram não configuradas.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})

def get_ultima_atividade():
    if not GOOGLE_CREDENTIALS:
        enviar_telegram("⚠️ Erro: ❌ GOOGLE_CREDENTIALS não encontrada.")
        return None, None

    import json
    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
    )

    service = build("drive", "v3", credentials=creds)
    try:
        file = service.files().get(
            fileId=FILE_ID,
            fields="modifiedTime, lastModifyingUser(permissionId)"
        ).execute()

        modified_time = file["modifiedTime"]
        permission_id = file.get("lastModifyingUser", {}).get("permissionId", "Desconhecido")
        nome = MAPA_PESSOAS.get(permission_id, "Desconhecido")

        dt_obj = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
        dt_brasil = dt_obj.astimezone(timezone(timedelta(hours=-3)))
        mod_formatado = dt_brasil.strftime("%d/%m/%Y %H:%M:%S")

        return mod_formatado, nome

    except Exception as e:
        enviar_telegram(f"⚠️ Erro monitoramento: {e}")
        return None, None
