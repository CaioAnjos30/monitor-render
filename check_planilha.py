from monitor_planilha import get_modified_time, enviar_telegram
import os

CAMINHO = "ultima_modificacao.txt"

def main():
    mod = get_modified_time()
    if not mod:
        print("❌ Não foi possível obter modificação.")
        return

    if os.path.exists(CAMINHO):
        with open(CAMINHO, "r") as f:
            atual = f.read().strip()
        if atual == mod:
            print("⏳ Nada novo. Última modificação já registrada.")
            return

    # Salva nova modificação
    with open(CAMINHO, "w") as f:
        f.write(mod)

    print(f"✅ Nova modificação detectada: {mod}")
    enviar_telegram(f"📢 A planilha foi modificada!\n🕒 Quando: {mod}")

if __name__ == "__main__":
    main()
