from monitor_planilha import get_modified_time
import os

CAMINHO = "ultima_modificacao.txt"

def main():
    mod = get_modified_time()
    if not mod:
        print("❌ Não foi possível obter modificação.")
        return

    with open(CAMINHO, "w") as f:
        f.write(f"{mod}|nao")

    print(f"✅ Última modificação salva: {mod}")

if __name__ == "__main__":
    main()
