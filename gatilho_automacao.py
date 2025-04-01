from datetime import datetime, timedelta
import os
from monitor_planilha import enviar_telegram

ARQUIVO_MODIFICACAO = 'ultima_modificacao.txt'
DELAY_MINUTOS = 5

def main():
    if not os.path.exists(ARQUIVO_MODIFICACAO):
        print("⏳ Aguardando primeira modificação...")
        return

    with open(ARQUIVO_MODIFICACAO, 'r') as f:
        conteudo = f.read().strip().split('|')
        horario_mod = conteudo[0]
        ja_executado = conteudo[1] if len(conteudo) > 1 else 'nao'

    if ja_executado == 'sim':
        print("⏱️ Já executado anteriormente para essa modificação.")
        return

    try:
        horario_dt = datetime.strptime(horario_mod, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        print("❌ Erro ao interpretar horário.")
        return

    agora = datetime.now()

    if agora - horario_dt >= timedelta(minutes=DELAY_MINUTOS):
        enviar_telegram("🤖 A automação foi executada com base na última modificação da planilha.")
        with open(ARQUIVO_MODIFICACAO, 'w') as f:
            f.write(f"{horario_mod}|sim")
        print("✅ Automação executada com sucesso!")
    else:
        print("⌛ Aguardando os 5 minutos de inatividade...")

if __name__ == '__main__':
    main()
