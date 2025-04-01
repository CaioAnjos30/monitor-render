import os
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from monitor_planilha import enviar_telegram

# ID da planilha do Google Drive
FILE_ID = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"

# Caminho para a variável de ambiente
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

# Mapa de permissionId para nome amigável
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

def get_ultima_atividade():
    if not GOOGLE_CREDENTIALS:
        enviar_telegram("⚠️ Erro: ❌ Variável de ambiente GOOGLE_CREDENTIALS não encontrada!")
        return None, None

    from google.oauth2.service_account import Credentials
    import json

    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
    )

    service = build("drive", "v3", credentials=creds)
    try:
        file = service.files().get(
            fileId=FILE_ID,
            fields="modifiedTime, lastModifyingUser(displayName, permissionId)"
        ).execute()

        modified_time = file.get("modifiedTime")
        user_info = file.get("lastModifyingUser", {})
        who = user_info.get("permissionId", "Desconhecido")
        nome = MAPA_PESSOAS.get(who, "Desconhecido")

        # Converte para fuso horário do Brasil (GMT-3)
        dt_obj = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
        dt_brasil = dt_obj.astimezone(timezone(timedelta(hours=-3)))
        data_formatada = dt_brasil.strftime("%d/%m/%Y %H:%M:%S")

        return data_formatada, nome

    except Exception as e:
        enviar_telegram(f"⚠️ Erro ao verificar a planilha: {e}")
        return None, None

def main():
    mod, quem = get_ultima_atividade()
    if not mod:
        print("❌ Não foi possível obter modificação.")
        return

    path = "ultima_modificacao.txt"
    mod_str = f"{mod}|sim"

    # Verifica o que estava salvo
    if os.path.exists(path):
        with open(path, "r") as f:
            atual = f.read().strip()
        if atual == mod_str:
            print("⏳ Nada novo. Última modificação já registrada.")
            return

    # Salva nova modificação
    with open(path, "w") as f:
        f.write(mod_str)

    print(f"✅ Nova modificação detectada: {mod_str}")
    enviar_telegram(f"📢 A planilha foi modificada!\n🧑‍💼 Quem: {quem}\n🕒 Quando: {mod}")

if __name__ == "__main__":
    main()
