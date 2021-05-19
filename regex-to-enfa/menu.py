import afne
from er_para_afne import *

def menu() -> None:
  afne_nome: str = "./afne_convertido.json"
  afne_exemplo: str = "exemplo_1"
  robocop: afne = afne.AFNE(afne_nome, afne_exemplo, True)

  afne_nome: str = "./afne_data.json"
  afne_exemplo: str = "exemplo_1"
  autobot: afne = afne.AFNE(afne_nome, afne_exemplo, True)

  print("Selecione a opção: ")
  print("1) AFNE")
  print("2) Conversor ER -> AFNE")
  print("3) AFNE Convertido")
  print("4) Sair")

  opcao_1: int = int(input("Opcao: "))

  while True:
    if opcao_1 == 1:
      autobot.show()
      while (True):        
        print('\n\n')
        entrada: str = input("Digite uma entrada (separe os simbolos por espaços ou digite 'sair'): ")

        if entrada.lower() == 'sair':
          break
        if autobot.verifica_cadeia(entrada):
          print("\033[32mCADEIA ACEITA!!!\033[0;0m\n")
        else:
          print("\033[31mCADEIA REJEITADA!!!\033[0;0m\n")
        print("="*128)
      print("Saindo . . .\n")  
      return
    elif opcao_1 == 2:
      automato: dict = {}
      expressao = str(input("Digite uma expressão (Digite 'sair' para sair): "))

      if expressao == 'sair':
        break
      automato = regex_to_afne(expressao)
      printa_automato(automato)

      print('*'*50)
      opcao_2 = str(input("Escrever no arquivo? [Y/N]: ")).lower()
      print('*'*50,'\n')

      if opcao_2 == 'y':
        escreve_no_arquivo(automato, expressao)
        print("Saindo :(\n")  
        return                       
    elif opcao_1 == 3:
      robocop.show()
      while (True):        
        print('\n\n')
        entrada: str = input("Digite uma entrada (separe os simbolos por espaços ou digite 'sair'): ")

        if entrada.lower() == 'sair':
          break
        if robocop.verifica_cadeia(entrada):
          print("\033[32mCADEIA ACEITA!!!\033[0;0m\n")
        else:
          print("\033[31mCADEIA REJEITADA!!!\033[0;0m\n")
        print("="*128)
      print("Saindo . . .\n")  
      return
    elif opcao_1 == 4:
      break           

menu()