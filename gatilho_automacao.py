import os
from datetime import datetime, timedelta
from monitor_planilha import get_modified_time, enviar_telegram

ARQUIVO_ULTIMA_MODIFICACAO = 'ultima_modificacao.txt'
ARQUIVO_ULTIMA_EXECUCAO = 'ultima_execucao.txt'
DELAY_MINUTOS = 5  # tempo de inatividade para considerar a execução

def ja_executou(horario_modificacao):
    if not os.path.exists(ARQUIVO_ULTIMA_EXECUCAO):
        return False
    with open(ARQUIVO_ULTIMA_EXECUCAO, 'r') as f:
        ultima_exec = f.read().strip()
    return ultima_exec == horario_modificacao

def main():
    ultima_mod = get_modified_time()
    if not ultima_mod:
        print("⚠️ Nenhuma modificação detectada.")
        return

    try:
        horario = datetime.strptime(ultima_mod, "%d/%m/%Y %H:%M:%S")
    except:
        print("❌ Erro ao converter horário.")
        return

    # Verifica se temos uma modificação anterior salva
    if os.path.exists(ARQUIVO_ULTIMA_MODIFICACAO):
        with open(ARQUIVO_ULTIMA_MODIFICACAO, 'r') as f:
            conteudo = f.read().strip()
            try:
                horario_salvo_str, status = conteudo.split("|")
            except:
                horario_salvo_str, status = "00/00/0000 00:00:00", "sim"
    else:
        horario_salvo_str, status = "00/00/0000 00:00:00", "sim"

    try:
        horario_salvo = datetime.strptime(horario_salvo_str, "%d/%m/%Y %H:%M:%S")
    except:
        horario_salvo = datetime.min

    if horario > horario_salvo:
        if datetime.now() - horario >= timedelta(minutes=DELAY_MINUTOS):
            if not ja_executou(ultima_mod):
                with open(ARQUIVO_ULTIMA_EXECUCAO, 'w') as f:
                    f.write(ultima_mod)
                with open(ARQUIVO_ULTIMA_MODIFICACAO, 'w') as f:
                    f.write(f"{ultima_mod}|sim")

                mensagem = f"📢 A planilha foi modificada!\n🕒 Quando: {ultima_mod}"
                enviar_telegram(mensagem)
                print("✅ Alerta enviado.")
            else:
                print("⏱️ Já executado anteriormente.")
        else:
            print("🕓 Aguardando tempo mínimo para envio.")
    else:
        print("🟡 Nenhuma nova modificação detectada.")

if __name__ == '__main__':
    main()
