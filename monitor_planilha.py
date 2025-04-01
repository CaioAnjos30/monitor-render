from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os
import json
import pytz
import requests

# ⏰ Timezone brasileiro
TZ = pytz.timezone("America/Sao_Paulo")

# ✅ Mapa de IDs para nomes legíveis
MAPA_PESSOAS = {
    "people/00289363581191441115": "python-planilhas@black-moon-455013-a5.iam.gserviceaccount.com",
    "people/01708069321338839734": "Olívia Scanentech",
    "people/04174463028638780853": "Enzo Silva",
    "people/04296532891180382301": "Breno Mattos",
    "people/15062355278509587252": "Caio Anjos",
    "people/18141613163935753002": "Mtiemy (Scanntech)",
}

# 📁 ID do arquivo da planilha
ID_ARQUIVO = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"

# 📩 Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN") or "SEU_TOKEN_AQUI"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "SEU_CHAT_ID_AQUI"

# 📄 Caminho para salvar modificação
ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'


def get_ultima_atividade():
    # 🔐 Autenticação
    creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.activity.readonly"]
    )

    service = build('driveactivity', 'v2', credentials=creds)

    body = {
        "itemName": f"items/{ID_ARQUIVO}",
        "pageSize": 1,
        "filter": "time > 2024-01-01T00:00:00Z"
    }

    response = service.activity().query(body=body).execute()
    activities = response.get("activities", [])

    if not activities:
        return None, None

    activity = activities[0]
    time = activity["timestamp"]
    quem = activity["actors"][0].get("user", {}).get("knownUser", {}).get("personName", "Desconhecido")

    # ⏱️ Ajusta para horário de Brasília
    dt_utc = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_brasil = dt_utc.replace(tzinfo=pytz.utc).astimezone(TZ)

    return quem, dt_brasil.strftime("%d/%m/%Y %H:%M:%S")


def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={
        'chat_id': CHAT_ID,
        'text': mensagem
    })


def main():
    try:
        quem, quando = get_ultima_atividade()

        if not quem or not quando:
            print("❌ Nenhuma modificação encontrada.")
            return

        # 🧠 Nome real se houver
        nome_legivel = MAPA_PESSOAS.get(quem, "Desconhecido")

        mensagem = (
            "📢 A planilha foi modificada!\n"
            f"👨‍💼 Quem: {nome_legivel}\n"
            f"🕒 Quando: {quando}"
        )

        enviar_telegram(mensagem)
        print("✅ Mensagem enviada com sucesso!")

        # 📝 Salva modificação local
        with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
            f.write(f"{quando}|nao")

    except Exception as e:
        print("❌ Erro ao monitorar:", e)
        enviar_telegram(f"⚠️ Erro no monitoramento:\n❌ {e}")


if __name__ == "__main__":
    main()
