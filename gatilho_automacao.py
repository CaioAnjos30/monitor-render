import os
from datetime import datetime, timedelta
from monitor_planilha import enviar_telegram, get_modified_time

ARQUIVO_ULTIMA_MODIFICACAO = "ultima_modificacao.txt"
ARQUIVO_ULTIMA_EXECUCAO = "ultima_execucao.txt"
DELAY_MINUTOS = 5  # Tempo de inatividade antes de rodar a automação

def ja_executou(horario_modificacao):
    if not os.path.exists(ARQUIVO_ULTIMA_EXECUCAO):
        return False
    with open(ARQUIVO_ULTIMA_EXECUCAO, "r") as f:
        ultima_exec = f.read().strip()
    return ultima_exec == horario_modificacao

def main():
    ultima_mod = get_modified_time()
    if not ultima_mod:
        print("⚠️ Nenhuma modificação detectada.")
        return

    try:
        horario = datetime.strptime(ultima_mod, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        print("❌ Erro ao converter data/hora da modificação.")
        return

    # Lê o valor salvo anteriormente
    if os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
        with open(ARQUIVO_ULTIMA_MODIFICACAO, "r") as f:
            horario_salvo_str = f.read().strip()
    else:
        horario_salvo_str = "00/00/0000 00:00:00"

    try:
        horario_salvo = datetime.strptime(horario_salvo_str, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        horario_salvo = datetime.min

    # Verifica se houve nova modificação e se já passou o tempo de delay
    if horario > horario_salvo:
        if datetime.now() - horario >= timedelta(minutes=DELAY_MINUTOS):
            if not ja_executou(ultima_mod):
                with open(ARQUIVO_ULTIMA_EXECUCAO, "w") as f:
                    f.write(ultima_mod)
                with open(ARQUIVO_ULTIMA_MODIFICACAO, "w") as f:
                    f.write(ultima_mod)

                mensagem = f"🤖 A automação foi executada com base na última modificação.\n🕒 Quando: {ultima_mod}"
                enviar_telegram(mensagem)
                print("✅ Automação executada e alerta enviado.")
            else:
                print("⏱️ Já executado para essa modificação.")
        else:
            print(f"🕓 Aguardando {DELAY_MINUTOS} minutos de inatividade.")
    else:
        print("🟡 Nenhuma nova modificação desde a última execução.")

if __name__ == "__main__":
    main()
