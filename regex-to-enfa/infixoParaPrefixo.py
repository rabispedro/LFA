# Convertendo da ordem infixa para a prefixa usando pilha
def reverte_expressao(expressao: str) -> str:
  return expressao[::-1]

def empilha(pilha: list, elemento: str) -> list:
  pilha.append(elemento)
  return pilha


def desempilha(pilha: list) -> None:
  pilha.pop()
  return


def pilha_vazia(pilha: list) -> bool:
  if pilha == []:
    return True
  return False


def topo_pilha_1(pilha: list):
  return pilha[-1]


def topo_pilha_2(pilha: list):
  return pilha[-2]  


def get_prioridade(elemento: str) -> int:
  if elemento == '+':
    return 1
  elif elemento == '.':
    return 2
  elif elemento == '*':
    return 3
  elif elemento == ')':           
    return -1


def lista_para_string(lista: list) -> str:
  novaString: str = ''
  for elemento in lista:
    novaString+=elemento
  return novaString


def eh_operador(elemento: str) -> bool:
  operadores: list = ['*', '.','+']
  if elemento in operadores:
    return True
  else:
    return False


def infixo_para_prefixo(expressao: str) -> str:
  entrada: str = reverte_expressao(expressao)
  pilha: list = []
  saida: list = []
  topo: str = ''
  parenteses: list = ['(', ')']

  for elemento in entrada:
    if not eh_operador(elemento):
      if elemento not in parenteses:
        saida.append(elemento)

      if elemento == ')':
        empilha(pilha, elemento)
        topo = elemento

      elif elemento == '(':
        while topo != ')':
          saida.append(topo)          
          desempilha(pilha)
          topo = pilha[-1]
        desempilha(pilha)
        if pilha_vazia(pilha):
          topo = ''

        else:
          topo = pilha[-1]
    else:        
      if pilha_vazia(pilha):
        topo = elemento
        empilha(pilha, elemento)

      elif get_prioridade(elemento) >= get_prioridade(topo):
        empilha(pilha, elemento)
        topo = elemento

      elif get_prioridade(elemento) < get_prioridade(topo):        
        while True:
          saida.append(topo)
          desempilha(pilha)
          if pilha_vazia(pilha):
            empilha(pilha, elemento)
            topo = pilha[-1]
            break
          else:
            topo = pilha[-1]
            if get_prioridade(topo) <= get_prioridade(elemento) :
              empilha(pilha, elemento)
              topo = pilha[-1]
              break

  # Percorreu toda a entrada
  # Desempilhar operadores restantes
  while pilha != []:
    topo = pilha[-1]
    saida.append(topo)
    desempilha(pilha)
  
  # Inverter saida
  saida = lista_para_string(saida)
  saida = reverte_expressao(saida)
  
  return saida
 
# Exemplos:
expressao_1:str = "(0.1)*+0.(1.0)*+1.(0.1)*+(1.0)*"
expressao_2:str = "0.1*+1"
expressao_3:str = "1*+1"
expressao_4:str = "0.(1*+1)"
expressao_5:str = "(0.1)*+1"

expressao_convertida = infixo_para_prefixo(expressao_5)