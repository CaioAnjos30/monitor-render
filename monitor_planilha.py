from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os
import json
import pytz
import requests
from sqlalchemy import create_engine

# Timezone Brasil
TZ = pytz.timezone("America/Sao_Paulo")

# Mapa de pessoas
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

ID_ARQUIVO = "1WjKXeS7lXkWW8rEFBdLRiBtAWEp-5vUT"
ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def salvar_log(usuario, tipo, mensagem):
    try:
        engine = create_engine(
            'postgresql://googledrive_postgree_user:zCjZp44UQ3MU4rAjmteL7DBWaxy3D6BU@dpg-cvikpkpr0fns73cl87cg-a.frankfurt-postgres.render.com:5432/googledrive_postgree'
        )
        with engine.begin() as conn:
            conn.execute(
                "INSERT INTO logs_monitoramento (data_hora, usuario, tipo, mensagem) VALUES (%s, %s, %s, %s)",
                (datetime.now(), usuario, tipo, mensagem)
            )
        print("📝 Log salvo no PostgreSQL")
    except Exception as e:
        print(f"⚠️ Erro ao salvar log: {e}")

def get_ultima_atividade():
    creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.activity.readonly"]
    )

    service = build('driveactivity', 'v2', credentials=creds)

    body = {
        "itemName": f"items/{ID_ARQUIVO}",
        "pageSize": 1
    }

    response = service.activity().query(body=body).execute()
    activities = response.get("activities", [])

    if not activities:
        return None, None

    activity = activities[0]
    time = activity["timestamp"]
    quem = activity["actors"][0].get("user", {}).get("knownUser", {}).get("personName", "Desconhecido")

    dt_utc = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_brasil = dt_utc.replace(tzinfo=pytz.utc).astimezone(TZ)
    data_formatada = dt_brasil.strftime("%d/%m/%Y %H:%M:%S")

    return quem, data_formatada

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': mensagem})

def ja_enviou(quando):
    if not os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
        return False
    with open(ARQUIVO_ULTIMA_MODIFICACAO, 'r') as f:
        conteudo = f.read().strip()
    return conteudo.startswith(quando)

def main():
    try:
        quem, quando = get_ultima_atividade()
        if not quem or not quando:
            print("⚠️ Nenhuma modificação encontrada.")
            return

        if ja_enviou(quando):
            print("⏱️ Modificação já notificada anteriormente.")
            return

        nome_legivel = MAPA_PESSOAS.get(quem, "Desconhecido")

        mensagem = (
            "📢 A planilha foi modificada!\n"
            f"👨‍💼 Quem: {nome_legivel}\n"
            f"🕒 Quando: {quando}"
        )
        enviar_telegram(mensagem)
        salvar_log(nome_legivel, "modificacao", f"Planilha modificada por {nome_legivel} às {quando}")

        with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
            f.write(f"{quando}|nao")

        print("✅ Mensagem enviada com sucesso!")

    except Exception as e:
        print("❌ Erro ao monitorar:", e)
        enviar_telegram(f"⚠️ Erro no monitoramento:\n❌ {e}")

if __name__ == "__main__":
    main()
