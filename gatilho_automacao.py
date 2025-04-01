from datetime import datetime, timedelta
import os
from monitor_planilha import enviar_telegram, salvar_log

ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'
ARQUIVO_ULTIMA_EXECUCAO = 'ultima_execucao.txt'
DELAY_MINUTOS = 5  # tempo de inatividade para rodar automação

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
        conteudo = f.read().strip()

    if "|" not in conteudo:
        print("❌ Formato inválido no arquivo de modificação.")
        return

    mod_str, status = conteudo.split("|")

    if status == "sim":
        print("⏭️ Modificação já processada.")
        return

    try:
        horario_mod = datetime.strptime(mod_str, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        print("❌ Formato de data inválido.")
        return

    agora = datetime.now()
    if agora - horario_mod >= timedelta(minutes=DELAY_MINUTOS):
        if ja_executou(mod_str):
            print("⏱️ Automação já foi executada para essa modificação.")
            return

        # (Aqui entraria seu processamento principal futuro, tipo atualizar planilha/dash/etc)
        enviar_telegram("🤖 A automação foi executada com base na última modificação da planilha.")
        salvar_log("Sistema", "automacao", f"Automação executada para modificação em {mod_str}")

        with open(ARQUIVO_ULTIMA_EXECUCAO, 'w') as f:
            f.write(mod_str)

        with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
            f.write(f"{mod_str}|sim")

        print("✅ Automação executada com sucesso!")

    else:
        print("🕒 Aguardando 5 minutos após a modificação...")

if __name__ == "__main__":
    main()
