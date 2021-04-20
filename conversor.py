import afnd
import afd
import afne
import ast

def list_to_str(items):
  string = "" 
  for item in items:
    # print("item: "+item)
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
      # print("regra: "+ str(regra))
      estado = regra[2]
      flag: bool = False
        
      flag = str(estado).replace('[', '').replace(']', '').replace('\'', '') in estados

      if flag:
        break
      else:
        print(str(estado).replace('[', '').replace(']', '').replace('\'', ''))
        estados.append(str(estado).replace('[', '').replace(']', '').replace('\'', ''))

    # print("estados: "+ str(estados))
    # for estado in estados:
    #   print("estado: "+ estado)
    automato.set_estados(estados)

    # converter estados finais
    estados_finais = []
    finais_afn = afn.get_estados_finais()
    list_estados = list_to_str(estados).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').strip('q0').split("|")
    list_estados.remove('')
    list_estados.remove('')
    
    # print("list_estados: " + str(list_estados))

    for estado in list_estados:
      # print("estado: "+str(estado))
      sub_estados = estado.split(',')
      for sub in sub_estados:
        # print("sub: \'"+ sub+"\'")
        if sub in finais_afn:
          estados_finais.append(estado)
    
    # print(estados_finais)
    automato.set_estados_finais(estados_finais)

    # converte funcao de transicao
    regras = []
    regras_afn = afn.get_funcao_transicao()

    for regra in regras_afn:
      for estado in list_estados:
        # print("estado: "+str(estado))
        regra_afd = estado + " " + regra[1] + " "
        estados_regra = []
        
        sub_estados = estado.split(',')
        for sub in sub_estados:
          # print("sub: \'"+ sub+"\'")
          str_regra = str(regra[2]).replace('[', '').replace(']', '').replace('\'', '')
          estados_regra.append(str_regra)
        
        estados_regra = str(list(set(estados_regra)))

        # print("estados_regra: "+ estados_regra )
        regra_afd += estados_regra

        # print("regra_afd: "+ str(regra_afd))
        regras.append(regra_afd)
    for regra in regras:
      print()
      print("regra: "+ str(regra))
        

    return

  def converteAFNE(self, afne):
    return
"""

estados afd
"q0" "[q0,q1]"

 CONVERSÃO AFNE -> AFD

  ["q1", "a", ["q0", "q2"]],
  ["q1", "&", ["q2"],
  ["q2", "&", ["q3"],
  ["q3", "&", ["q5"]
  ["q3", "b", ["q0", "q2"]],

  ["q0", "q2"] => "qA"
  e-fecho("q1") => ["q1", "q2", "q3", "q5"]
  
  ["q1", "a", ["qA"]],
  ["q1", "&", ["q1", "q2", "q3", "q5"]]


  delta [0, 1, 2]
  se ( len( atual[i][2]) > 1 ):
      flag: bool = False
      
      for estado in atual[i][2]:
          flag = (estado in LISTA DE ESTADOS NOVOS)
      
      if(flag):
          #    Estado Novo ja foi feito
          break
      else:
          #    PRECISA CRIAR UM NOVO ESTADO
"""