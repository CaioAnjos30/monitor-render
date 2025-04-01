import os
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

# === VARIÁVEIS DE AMBIENTE ===
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ARQUIVO_MODIFICACAO = 'ultima_modificacao.txt'

# === CONFIGURAÇÃO ===
FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"

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
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Variáveis do Telegram não configuradas.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensagem})
    if response.status_code == 200:
        print("📨 Mensagem enviada com sucesso.")
    else:
        print(f"❌ Falha ao enviar mensagem: {response.text}")


def get_ultima_atividade():
    if not GOOGLE_CREDENTIALS:
        enviar_telegram("⚠️ Erro: ❌ GOOGLE_CREDENTIALS não encontrada.")
        return None, None

    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
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

        # Ajusta para horário de Brasília
        dt_obj = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
        dt_brasil = dt_obj.astimezone(timezone(timedelta(hours=-3)))
        mod_formatado = dt_brasil.strftime("%d/%m/%Y %H:%M:%S")

        return mod_formatado, nome

    except Exception as e:
        enviar_telegram(f"⚠️ Erro no monitoramento: {e}")
        return None, None


def main():
    data_mod, quem = get_ultima_atividade()
    if not data_mod:
        print("⛔ Nenhuma modificação detectada.")
        return

    mod_str = f"{data_mod}|sim"

    if os.path.exists(ARQUIVO_MODIFICACAO):
        with open(ARQUIVO_MODIFICACAO, "r") as f:
            atual = f.read().strip()
        if atual == mod_str:
            print("⏳ Nenhuma nova modificação.")
            return

    with open(ARQUIVO_MODIFICACAO, "w") as f:
        f.write(mod_str)

    mensagem = (
        "📢 A planilha foi modificada!\n"
        f"🧑‍💼 Quem: {quem}\n"
        f"🕒 Quando: {data_mod}"
    )
    enviar_telegram(mensagem)
    print(f"✅ Modificação registrada e alerta enviado: {mensagem}")


if __name__ == "__main__":
    main()
