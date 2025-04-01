from monitor_planilha import get_modified_time, enviar_telegram
import os

ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'

def main():
    try:
        atual = get_modified_time()

        if os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'r') as f:
                ultima = f.read().strip()
        else:
            ultima = ""

        if atual != ultima:
            enviar_telegram("📢 A planilha base foi atualizada com sucesso! ✅")
            with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
                f.write(atual)
        else:
            print("🕒 Sem alteração detectada.")
    except Exception as e:
        enviar_telegram(f"⚠️ Erro no monitoramento: {e}")

if __name__ == '__main__':
    main()
