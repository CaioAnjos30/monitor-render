import os
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from monitor_planilha import enviar_telegram

# ID do arquivo .xlsx no Google Drive
FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"

# Variável de ambiente com as credenciais
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

# Caminho do arquivo de controle
ARQUIVO_MODIFICACAO = "ultima_modificacao.txt"

def get_modified_time():
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
    # Converter UTC → horário de Brasília
    dt = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
    dt_brasil = dt.astimezone(timezone(timedelta(hours=-3)))
    return dt_brasil.strftime("%d/%m/%Y %H:%M:%S")

def main():
    mod = get_modified_time()
    if not mod:
        print("❌ Não foi possível obter modificação.")
        return

    # Comparar com data anterior
    if os.path.exists(ARQUIVO_MODIFICACAO):
        with open(ARQUIVO_MODIFICACAO, "r") as f:
            atual = f.read().strip()
        if atual == mod:
            print("⏳ Nada novo. Última modificação já registrada.")
            return

    # Atualiza o arquivo com nova data
    with open(ARQUIVO_MODIFICACAO, "w") as f:
        f.write(mod)

    print(f"✅ Nova modificação detectada: {mod}")
    enviar_telegram(f"📢 A planilha foi modificada!\n🕒 Quando: {mod}")

if __name__ == "__main__":
    main()
