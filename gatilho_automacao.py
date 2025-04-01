from datetime import datetime, timedelta
import os
from monitor_planilha import enviar_telegram

ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'
ARQUIVO_ULTIMA_EXECUCAO = 'ultima_execucao.txt'
DELAY_MINUTOS = 5  # tempo de inatividade para considerar rodar automação

def ja_executou(horario_modificacao):
    if not os.path.exists(ARQUIVO_ULTIMA_EXECUCAO):
        return False
    with open(ARQUIVO_ULTIMA_EXECUCAO, 'r') as f:
        ultima_exec = f.read().strip()
    return ultima_exec == horario_modificacao

def main():
    if not os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
        print("🟡 Nenhuma modificação registrada ainda.")
        return

    with open(ARQUIVO_ULTIMA_MODIFICACAO, 'r') as f:
        mod_str = f.read().strip()

    try:
        horario_mod = datetime.strptime(mod_str, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        print("❌ Formato inválido da data de modificação.")
        return

    agora = datetime.now()
    if agora - horario_mod >= timedelta(minutes=DELAY_MINUTOS):
        if ja_executou(mod_str):
            print("⏱️ Automação já foi executada para essa modificação.")
            return

        # Aqui você pode chamar seu script de automação real, por exemplo:
        # import main
        # main.run()

        enviar_telegram("🤖 A automação foi executada com base na última modificação da planilha.")
        with open(ARQUIVO_ULTIMA_EXECUCAO, 'w') as f:
            f.write(mod_str)
        print("✅ Automação executada com sucesso!")
    else:
        print("🕒 Aguardando 5 minutos após modificação...")

if __name__ == '__main__':
    main()
