from infixoParaPrefixo import *
from copy import deepcopy
import json

def gera_estados(quantidade_estados: int) -> list:
  """
  Recebe uma quantidade e retorna uma lista com nomes de estados
  """
  estados: list = []

  for i in range(quantidade_estados):
    estados.append('q'+str(i))    
  return estados


def cria_automato_unico(simbolo: str) -> dict:
  """
  Recebe um simbolo e retorna o seu automato em formato de quintupla(dict)
  """

  estados = gera_estados(2)
  estado_inicial = estados[0]
  estado_final = [estados[1]]

  funcao_transicao: list = [] 
  funcao_transicao.append([estado_inicial, simbolo, estado_final])

  automato: dict = {
    "alfabeto":[simbolo],
    "estados": estados,
    "estado_inicial": estado_inicial,
    "estados_finais": estado_final,
    "funcao_transicao": funcao_transicao
  }

  return automato


def retira_repetidos(automato_1: dict, automato_2: dict) -> dict:
  """
  Recebe dois automatos e retorna a 5-tupla do automato_2 sem os estados repetidos
  """

  antigo_automato_2: dict = deepcopy(automato_2)
  novo_automato_2: dict = deepcopy(automato_2)   

  j: int = 1
  numero_estado: int = 0

  # renomeia estados
  for i, estado_2 in enumerate(automato_2['estados']):
    if len(automato_1['estados'][-1]) > 2:
      numero_estado = int(automato_1['estados'][-1][1] + automato_1['estados'][-1][2])+j
    elif len(automato_1['estados'][-1]) > 3:
      numero_estado = int(automato_1['estados'][-1][1] + automato_1['estados'][-1][2] +automato_1['estados'][-1][3])+j 
    else:
      numero_estado = int(automato_1['estados'][-1][1])+j
    novo_automato_2['estados'][i] = 'q'+ str(numero_estado)
    j+=1    

  nova_funcao_transicao_2: list = []

  # renomeia funcao transicao
  novos_estados_2: list = novo_automato_2['estados']
  antigos_estados_2: list = antigo_automato_2['estados']

  for regra in antigo_automato_2['funcao_transicao']:
    i = antigos_estados_2.index(regra[0])
    if regra[2] != []:
      k: int = 0
      saida: list = []
      for regra_interna in regra[2]:
        j = antigos_estados_2.index(regra[2][k])
        saida.append(novos_estados_2[j])
        k+=1
    else:
      saida = []
    entrada = novos_estados_2[i]
    nova_funcao_transicao_2.append([entrada, regra[1], saida])


  # renomeia estados finais
  antigos_estados_finais_2: list = antigo_automato_2['estados_finais']
  novos_estados_finais_2: list = []

  for estado_final in antigos_estados_finais_2:
    i = antigos_estados_2.index(estado_final)
    novos_estados_finais_2.append(novos_estados_2[i])

  # renomeia estado inicial
  antigo_estado_inicial_2: str = antigo_automato_2['estado_inicial']
  i = antigos_estados_2.index(antigo_estado_inicial_2)
  novo_estado_inicial_2: str = novos_estados_2[i]  

  novo_automato_2['estados'] = novos_estados_2
  novo_automato_2['estado_inicial'] = novo_estado_inicial_2
  novo_automato_2['estados_finais'] = novos_estados_finais_2
  novo_automato_2['funcao_transicao'] = nova_funcao_transicao_2

  novo_automato_1 = automato_1

  return [novo_automato_1, novo_automato_2]


def concatena(automato_1: dict, automato_2: dict) -> dict:
  """
  Recebe dois automatos e retorna um novo automato com eles concatenados
  """  
  novo_automato: list = retira_repetidos(automato_1, automato_2)
  novo_automato_1: dict = novo_automato[0]
  novo_automato_2: dict = novo_automato[1]
  novo_automato_3: dict = {}

  # une e cria alfabeto
  novo_automato_3['alfabeto'] = novo_automato_1['alfabeto'].copy()
  for alfabeto_2 in novo_automato_2['alfabeto']:
    if alfabeto_2 not in novo_automato_3['alfabeto']:
      novo_automato_3['alfabeto'].append(alfabeto_2)
  
  # une e cria estados
  novo_automato_3['estados'] = novo_automato_1['estados'] + novo_automato_2['estados']

  # cria estado inicial
  novo_automato_3['estado_inicial'] = novo_automato_1['estado_inicial']

  #cria estados finais
  novo_automato_3['estados_finais'] = novo_automato_2['estados_finais'].copy()

  # cria funcao transicao
  regras_conexoes: list = []
  for regra in novo_automato_1['estados_finais']:
    regras_conexoes.append([regra, '&', [novo_automato_2['estado_inicial']]])
    
  novo_automato_3['funcao_transicao'] = novo_automato_1['funcao_transicao'].copy() + novo_automato_2['funcao_transicao'].copy()
  novo_automato_3['funcao_transicao'] += regras_conexoes

  for i, regra in enumerate(novo_automato_3['funcao_transicao']):
    for regra_conexao in regras_conexoes:
      if regra_conexao[0] == regra[0] and regra_conexao[1] == regra[1] and regra[2] == []:
        novo_automato_3['funcao_transicao'].remove(novo_automato_3['funcao_transicao'][i])
  return novo_automato_3


def fechamento(automato: dict) -> dict:  
  """
  Recebe um automato e retorna o automato do seu fechamento
  """

  automato_aux: dict = {}
  automato_aux['estados'] = ['q0']

  antigo_automato: dict = deepcopy(retira_repetidos(automato_aux, automato)[1])
  novo_automato: dict = deepcopy(retira_repetidos(automato_aux, automato)[1])  

  # conecta estados finais ao estado inicial
  novas_regras: list = []
  for estado_final in antigo_automato['estados_finais']:
    novas_regras.insert(0,[estado_final, '&', [antigo_automato['estado_inicial']]])
  
  # cria novo estado inicial
  novo_estado_inicial: str = 'q0'

  novas_regras.append([novo_estado_inicial, '&', [antigo_automato['estado_inicial']]])

  # atualiza o automato
  novo_automato['estados'] = [novo_estado_inicial] + antigo_automato['estados']
  novo_automato['estados_finais'] = [novo_estado_inicial] + antigo_automato['estados_finais']
  novo_automato['estado_inicial'] = novo_estado_inicial
  novo_automato['funcao_transicao'] = antigo_automato['funcao_transicao'] + novas_regras
  
  return  novo_automato


def uniao(automato_1: dict, automato_2: dict):
  """
  Recebe dois automatos e retorna um automato com a união dos dois
  """
  novo_automato = retira_repetidos(automato_1, automato_2)

  novo_automato_1:dict = deepcopy(novo_automato[0])
  novo_automato_2:dict = deepcopy(novo_automato[1])
  novo_automato_3: dict = {}

  # cria estado inicial
  if len(novo_automato_2['estados'][-1]) > 2:
    numero_estado = int(novo_automato_2['estados'][-1][1] + novo_automato_2['estados'][-1][2])+1
  elif len(novo_automato_2['estados'][-1]) > 3:
    numero_estado = int(novo_automato_2['estados'][-1][1] + novo_automato_2['estados'][-1][2] + novo_automato_2['estados'][-1][3])+1
  else:
    numero_estado: int = int(novo_automato_2['estados'][-1][1]) + 1
  novo_estado_inicial: str = 'q' + str(numero_estado)

  # conecta o novo estado aos iniciais dos outros automatos
  novas_regras: list = []
  novas_regras.append([novo_estado_inicial, '&', [novo_automato_1['estado_inicial']]])
  novas_regras.append([novo_estado_inicial, '&', [novo_automato_2['estado_inicial']]])

  # atualiza o automato
  novo_automato_3['alfabeto'] = novo_automato_1['alfabeto'].copy()
  for alfabeto_2 in novo_automato_2['alfabeto']:
    if alfabeto_2 not in novo_automato_3['alfabeto']:
      novo_automato_3['alfabeto'].append(alfabeto_2)
  
  novo_automato_3['estados'] = novo_automato_1['estados'] + novo_automato_2['estados'] + [novo_estado_inicial]
  novo_automato_3['estado_inicial'] = novo_estado_inicial
  novo_automato_3['estados_finais'] = novo_automato_1['estados_finais'] + novo_automato_2['estados_finais']
  novo_automato_3['funcao_transicao'] = novo_automato_1['funcao_transicao'] + novo_automato_2['funcao_transicao'] + novas_regras

  return novo_automato_3


def printa_automato(automato: dict) -> None:
  print('alfabeto: ', automato['alfabeto'])
  print('estados: ', automato['estados'])
  print('estado inicial: ', automato['estado_inicial'])
  print('estados finais: ', automato['estados_finais'])  
  print('\nFunção transição: \n')
  for regra in automato['funcao_transicao']:
    print(regra)
  print('='*30)
  print()
  return        


def regex_to_afne(expressao: str):
  """
  Recebe uma expressão regular e retorna um AFNE correspodente
  """  
  pilha = []
  expressao = infixo_para_prefixo(expressao)
  expressao = reverte_expressao(expressao)
  automato = None
  entrada = []

  for elemento in expressao:
    if not eh_operador(elemento):
      automato = cria_automato_unico(elemento)
      entrada.append(automato)
    else:
      entrada.append(elemento)

  for elemento in entrada:
    if eh_operador(elemento):
      if elemento == '+':
        automato = uniao(dict(pilha[-1]), dict(pilha[-2]))        
        desempilha(pilha)
        desempilha(pilha)
        empilha(pilha, automato)      
      if elemento == '*':
        automato = fechamento(dict(pilha[-1]))
        desempilha(pilha)
        empilha(pilha, automato)
      if elemento == '.':
        automato = concatena(dict(pilha[-1]), dict(pilha[-2]))
        desempilha(pilha)
        desempilha(pilha)
        empilha(pilha, automato)
    else:
      empilha(pilha, elemento)    
  automato_final = pilha[0]
  automato_final = formata_funcao_transicao(automato_final)       
  return automato_final


def formata_funcao_transicao(automato: dict) -> dict:
  """
  Recebe um automato e o retorna com sua função transição formatada
  """
  antigo_automato = deepcopy(automato)
  novo_automato = deepcopy(automato)
  nova_funcao_transicao_aux = []    
  nova_funcao_transicao = []

  # Agrupando estados com mesmas saidas
  for regra in novo_automato['funcao_transicao']:
    nova_funcao_transicao_aux.append(regra[:2])
    nova_funcao_transicao_aux.append(regra[2])

  for i in range(0,len(nova_funcao_transicao_aux),2):
    entradas = nova_funcao_transicao_aux[i]
    saida = nova_funcao_transicao_aux[i+1]

    if entradas not in nova_funcao_transicao:
      nova_funcao_transicao.append(entradas)
      nova_funcao_transicao.append(saida)
    else:
      j = nova_funcao_transicao.index(entradas)
      nova_funcao_transicao[j+1] += saida  
  
  novo_automato['funcao_transicao'] = []
  for i in range(0,len(nova_funcao_transicao),2):
    entradas = nova_funcao_transicao[i]
    saida = nova_funcao_transicao[i+1]
    regra = entradas + [saida]
    novo_automato['funcao_transicao'].append(regra)

  # Adicionando novas regras
  regras_entradas = []
  regras_base = []
  novas_regras = []
  for estado in automato['estados']:
    for simbolo in automato['alfabeto']:
      regras_base.append([estado,simbolo])

  for regra in antigo_automato['funcao_transicao']:
    regras_entradas.append([regra[0],regra[1]])  

  for regra_base in regras_base:
    if regra_base not in regras_entradas:
      novas_regras.append(regra_base + [[]])   

  for nova_regra in novas_regras:
    novo_automato['funcao_transicao'].append(nova_regra)  
  
  # Ordenar   
  numeros_estados: list = []
  for estado in novo_automato['estados']:
    numeros_estados.append(int(estado[1:]))
  numeros_estados.sort()

  nova_funcao_transicao: list = []  
  for i,numero_estado in enumerate(numeros_estados):
    for regra in novo_automato['funcao_transicao']:
      if int(regra[0][1:]) == numeros_estados[i]:
        nova_funcao_transicao.append(regra)

  novo_automato['funcao_transicao'] = nova_funcao_transicao
  return novo_automato


def escreve_no_arquivo(automato: dict, expressao: str):

  dicionario =  {
    "exemplo_1":{
        "descricao":expressao,
        "alfabeto": automato['alfabeto'],
        "estados": automato['estados'],
        "estado_inicial": automato['estado_inicial'],
        "estados_finais": automato['estados_finais'],
        "funcao_transicao": automato['funcao_transicao']
    }
  }

  json_object = json.dumps(dicionario, indent = 1)
  with open("afne_convertido.json", "w") as outfile:
    outfile.write(json_object)
  return


# Exemplos:
expressao_1:str = "(0.1)*+0.(1.0)*+1.(0.1)*+(1.0)*"
expressao_2:str = "0.1*+1"
expressao_3:str = "1*+1"
expressao_4:str = "0.(1*+1)"
expressao_5:str = "(0.1)*+1"