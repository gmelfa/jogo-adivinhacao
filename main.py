import random

def main():
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    max_tentativas = 10
    
    print("=" * 30)
    print("Bem-vindo ao jogo de adivinhação!")
    print("Tente adivinhar um número entre 1 e 100.")
    print(f"Você tem {max_tentativas} tentativas.")
    print("=" * 30)

    for rodada in range(1, max_tentativas + 1):
        print(f"\nTentativa {rodada} de {max_tentativas}")
        try:
            palpite = int(input("Digite seu palpite: "))
            
            if palpite < 1 or palpite > 100:
                print("Digite um número entre 1 e 100!")
                continue
                
            tentativas += 1
            
            if palpite < numero_secreto:
                print("Tente um número MAIOR.")
            elif palpite > numero_secreto:
                print("Tente um número MENOR.")
            else:
                print(f"\nPARABÉNS! Você acertou em {tentativas} tentativas!")
                break
                
        except ValueError:
            print("Entrada inválida. Digite apenas números!")
    
    if palpite != numero_secreto:
        print(f"\nGame over! O número secreto era {numero_secreto}.")

if __name__ == "__main__":
    main()
