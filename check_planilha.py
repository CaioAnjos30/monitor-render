import os
from monitor_planilha import get_ultima_atividade, enviar_telegram

ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'

def main():
    try:
        horario_atual, usuario = get_ultima_atividade()

        # Verifica se já existe modificação registrada
        if os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'r') as f:
                ultima = f.read().strip().split('|')[0]  # pega só a data/hora
        else:
            ultima = ""

        if horario_atual != ultima:
            mensagem = (
                "📢 A planilha foi modificada!\n"
                f"🧑‍💼 Quem: {usuario}\n"
                f"🕒 Quando: {horario_atual}"
            )
            enviar_telegram(mensagem)

            # Salva nova modificação com status "nao"
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
                f.write(f"{horario_atual}|nao")
        else:
            print("🟢 Nenhuma nova modificação detectada.")

    except Exception as e:
        enviar_telegram(f"⚠️ Erro no monitoramento: ❌ {e}")
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    main()
