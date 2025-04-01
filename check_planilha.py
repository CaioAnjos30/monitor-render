import os
from monitor_planilha import get_ultima_atividade, enviar_telegram

ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'

def main():
    try:
        horario_atual, usuario = get_ultima_atividade()

        if os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'r') as f:
                ultima = f.read().strip().split('|')[0]  # Pega só o horário
        else:
            ultima = ""

        if horario_atual != ultima:
            mensagem = (
                "📢 A planilha foi modificada!\n"
                f"🧑‍💼 Quem: {usuario}\n"
                f"🕒 Quando: {horario_atual}"
            )
            enviar_telegram(mensagem)
            # Salva novo horário e flag de execução como "nao"
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
                f.write(f"{horario_atual}|nao")
        else:
            print("🟢 Nenhuma nova modificação detectada.")
    except Exception as e:
        enviar_telegram(f"⚠️ Erro no monitoramento: ❌ {e}")
