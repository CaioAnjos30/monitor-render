import os
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from monitor_planilha import enviar_telegram

# ID do arquivo no Google Drive
FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
ARQUIVO_ULTIMA_MODIFICACAO = "ultima_modificacao.txt"

def get_modified_time():
    if not GOOGLE_CREDENTIALS:
        enviar_telegram("⚠️ Erro: ❌ Variável de ambiente GOOGLE_CREDENTIALS não encontrada.")
        return None

    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
    )

    service = build("drive", "v3", credentials=creds)
    try:
        file = service.files().get(fileId=FILE_ID, fields="modifiedTime").execute()
        modified_time = file.get("modifiedTime")

        # Converter horário UTC para horário de Brasília
        dt = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
        dt_brasil = dt.astimezone(timezone(timedelta(hours=-3)))
        return dt_brasil.strftime("%d/%m/%Y %H:%M:%S")

    except Exception as e:
        enviar_telegram(f"⚠️ Erro ao verificar modificação: {e}")
        return None

def main():
    nova_data = get_modified_time()
    if not nova_data:
        print("❌ Não foi possível obter modificação.")
        return

    # Verifica se houve mudança comparada ao que estava salvo
    if os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
        with open(ARQUIVO_ULTIMA_MODIFICACAO, "r") as f:
            ultima = f.read().strip()
        if ultima == nova_data:
            print("⏳ Nenhuma nova modificação detectada.")
            return

    # Salva nova data
    with open(ARQUIVO_ULTIMA_MODIFICACAO, "w") as f:
        f.write(nova_data)

    print(f"✅ Nova modificação registrada: {nova_data}")
    enviar_telegram(f"📢 A planilha foi modificada!\n🕒 Quando: {nova_data}")

if __name__ == "__main__":
    main()
