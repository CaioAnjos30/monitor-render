from datetime import datetime, timedelta
import os
from monitor_planilha import enviar_telegram

ARQUIVO_MODIFICACAO = 'ultima_modificacao.txt'
DELAY_MINUTOS = 5  # Tempo de inatividade antes de rodar automação

def main():
    if not os.path.exists(ARQUIVO_MODIFICACAO):
        print("⏳ Aguardando primeira modificação...")
        return

    with open(ARQUIVO_MODIFICACAO, 'r') as f:
        conteudo = f.read().strip().split('|')
        if len(conteudo) != 2:
            print("⚠️ Formato inválido em ultima_modificacao.txt")
            return

        horario_str, status_execucao = conteudo
        if status_execucao == 'sim':
            print("⏱️ Automação já foi executada para essa modificação.")
            return

    try:
        horario_dt = datetime.strptime(horario_str, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        print("❌ Erro ao interpretar horário.")
        return

    agora = datetime.now()
    if agora - horario_dt >= timedelta(minutes=DELAY_MINUTOS):
        # ✅ Aqui você executaria seu script real de automação
        # import main
        # main.run()

        enviar_telegram("🤖 A automação foi executada com base na última modificação da planilha.")
        with open(ARQUIVO_MODIFICACAO, 'w') as f:
            f.write(f"{horario_str}|sim")
        print("✅ Automação executada com sucesso!")
    else:
        print("⌛ Aguardando os 5 minutos de inatividade...")

if __name__ == '__main__':
    main()
