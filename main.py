import random

def escolher_dificuldade():
    print("\n=== ESCOLHA A DIFICULDADE ===")
    print("1 - Fácil (20 tentativas)")
    print("2 - Médio (10 tentativas)")
    print("3 - Difícil (5 tentativas)")
    
    while True:
        escolha = input("Digite o número da dificuldade: ")
        if escolha == '1':
            return 20
        elif escolha == '2':
            return 10
        elif escolha == '3':
            return 5
        else:
            print("Opção inválida. Tente novamente.")

def menu_reiniciar():
    while True:
        resposta = input("\nDeseja jogar novamente? (s/n): ").lower()
        if resposta == 's':
            return True
        elif resposta == 'n':
            return False
        else:
            print("Digite 's' para sim ou 'n' para não.")

def jogar(max_tentativas):
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    
    print("\n" + "=" * 30)
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
                return True
                
        except ValueError:
            print("Entrada inválida. Digite apenas números!")
    
    print(f"\nGame over! O número secreto era {numero_secreto}.")
    return False

def main():
    print("\n*** JOGO DE ADIVINHAÇÃO ***\n")
    
    while True:
        # Escolher dificuldade
        max_tentativas = escolher_dificuldade()
        
        # Jogar o jogo
        jogar(max_tentativas)
        
        # Verificar se o jogador quer jogar novamente
        if not menu_reiniciar():
            print("\nObrigado por jogar! Até a próxima!")
            break

if __name__ == "__main__":
    main()
