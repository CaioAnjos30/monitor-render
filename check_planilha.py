import os
from monitor_planilha import get_ultima_atividade, enviar_telegram

ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'

def main():
    try:
        horario_atual, usuario = get_ultima_atividade()

        if os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'r') as f:
                ultima = f.read().strip()
        else:
            ultima = ""

        if horario_atual != ultima:
            mensagem = (
                "📢 A planilha foi modificada!\n"
                f"🧑‍💼 Quem: {usuario}\n"
                f"🕒 Quando: {horario_atual}"
            )
            enviar_telegram(mensagem)
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
                f.write(horario_atual)
        else:
            print("🕒 Nenhuma modificação detectada.")
    except Exception as e:
        enviar_telegram(f"⚠️ Erro no monitoramento: ❌ {e}")

if __name__ == '__main__':
    main()
