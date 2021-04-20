import afnd
import afd
import afne
import ast
import json

def escreve_no_arquivo(descricao, alfabeto, estados, estado_inicial, estados_finais, funcao_transicao):
  dicionario =  {
      "exemplo_1":{"descricao": descricao,
      "alfabeto": alfabeto,
      "estados": estados,
      "estado_inicial": estado_inicial,
      "estados_finais": estados_finais,
      "funcao_transicao": funcao_transicao}
  }
  json_object = json.dumps(dicionario)
  with open("testes.json", "w") as outfile:
    outfile.write(json_object)
  return


def formata_funcao_transicao(regras):
  nova_funcao_transicao = []
  for regra in regras:
    lst = regra.replace("'","").replace(", ",",").split(" ")
    nova_funcao_transicao.append(lst)
  return nova_funcao_transicao

def list_to_str(items):
  string = "" 
  for item in items:
    string += str(item) + "|"
  
  return string

class Conversor:

  def converteAFND(self, afn):
    automato = afd.AFD("","",False)
    automato.set_alfabeto(afn.get_alfabeto())
    automato.set_estado_inicial(afn.get_estado_inicial())
    automato.set_descricao("AFD Convertido com base no AFN: " + afn.get_descricao())

    estados: str = []
    estados.append("[\'" +automato.get_estado_inicial()+"\']")

    # converter estados
    for regra in afn.get_funcao_transicao():
      estado = regra[2]
      flag: bool = False
        
      flag = str(estado).replace('[', '').replace(']', '').replace('\'', '') in estados

      if flag:
        break
      else:
        estados.append(str(estado).replace('[', '').replace(']', '').replace('\'', ''))

    automato.set_estados(estados)

    # converter estados finais
    estados_finais = []
    finais_afn = afn.get_estados_finais()
    list_estados = list_to_str(estados).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').strip('q0').split("|")
    list_estados.remove('')
    list_estados.remove('')

    for estado in list_estados:
      sub_estados = estado.split(',')
      for sub in sub_estados:

        if sub in finais_afn:
          estados_finais.append(estado)
    

    automato.set_estados_finais(estados_finais)

    # converte funcao de transicao
    regras = []
    regras_afn = afn.get_funcao_transicao()

    for regra in regras_afn:
      for estado in list_estados:
        regra_afd = estado + " " + regra[1] + " "
        estados_regra = []
        sub_estados = estado.split(',')

        for sub in sub_estados:
          str_regra = str(regra[2]).replace('[', '').replace(']', '').replace('\'', '')
          estados_regra.append(str_regra)
      
        estados_regra = str(list(set(estados_regra)))
        regra_afd += estados_regra
        regras.append(regra_afd)

    nova_funcao_transicao = formata_funcao_transicao(regras)
    escreve_no_arquivo(automato.get_descricao(),automato.get_alfabeto(),automato.get_estados(),automato.get_estado_inicial(),automato.get_estados_finais(),nova_funcao_transicao)
    return