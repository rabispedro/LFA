import afnd
import afd
import afne
import ast
import json

def escreve_no_arquivo(descricao, alfabeto, estados, estado_inicial, estados_finais, funcao_transicao):
    for i in range(len(funcao_transicao)):
        funcao_transicao[i][2] = [funcao_transicao[i][2]]

    dicionario =  {
            "exemplo_1":{
                "descricao": descricao,
                "alfabeto": alfabeto,
                "estados": estados,
                "estado_inicial": estado_inicial,
                "estados_finais": estados_finais,
                "funcao_transicao": funcao_transicao
            }
    }
    json_object = json.dumps(dicionario, indent = 2)
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

def agrupa_estados(estado):
	return str(estado).replace("[", "").replace(",","").replace("]","").replace("\'","").replace(" ","-")

class Conversor:
	def afnd_to_afd(self, afnd):
			automato = afd.AFD("", "", False)
			automato.set_alfabeto(afnd.get_alfabeto())
			automato.set_estado_inicial(afnd.get_estado_inicial())
			automato.set_descricao("AFD convertido com base no AFND: "+afnd.get_descricao())
			# print(afnd.get_descricao())
			print("regras_afnd: "+str(afnd.get_funcao_transicao()))
			
			estados: list = afnd.get_estados()
			regras_afd: list = []
			
			# converter regras
			regras_afnd = afnd.get_funcao_transicao()
			for regra_afnd in regras_afnd: # percorre as regras do AFND e converte uma a uma
				# print(str(regra_afnd))
				
				# regra_afnd['q0' , '0' , '[q0, q1]']
				# converte estado da regra
				estado = regra_afnd[0]
				if not estado in estados:
					estados.append(estado)

				# converte estados resultantes
				estado = agrupa_estados(regra_afnd[2])
				# print(str(estado))
				if not estado in estados:
					estados.append(estado)

				# add a regra
				regra_afd: list = []
				regra_afd.append(regra_afnd[0])
				regra_afd.append(regra_afnd[1])
				regra_afd.append(estado)

				# add regra ao vetor de regras do afd
				if regra_afd != '' and not regra_afd in regras_afd:
					regras_afd.append(regra_afd)

				# print(str(regra_afd))

				# verificar casos do tipo ['q0','q1']
				# converter os sub estados gerados
				for est in estados:
					# print("est: "+ str(est))
					# print('regras_afd: ', str(regras_afd))
					for alfa in afnd.get_alfabeto():
						for regra in regras_afd:
							# print('regra: '+ str(regra))

							# verificar se o estado com o simbolo do alfabeto já está como regra
							# no vetor de regras do afd convertido
							if regra[0] == est and regra[1] == alfa: 
								break
							
							novos_estados: list = []
							sub_estados = str(est).split('-')

							# buscar a regra especifica de cada estado no AFND que gerou o estado atual no AFD
							# e concatenar os subestados
							for sub in sub_estados:
								# print('sub: '+sub)
								for afnd_regra in regras_afnd:
									if afnd_regra[0] == sub and afnd_regra[1] == alfa:
										for novo_estado in afnd_regra[2]:
											if not novo_estado in novos_estados:
												novos_estados.append(novo_estado)
							
							nova_regra_afd: list = []
							nova_regra_afd.append(est)
							nova_regra_afd.append(alfa)
							nova_regra_afd.append(agrupa_estados(novos_estados))

							# adicionar o novo estado gerado da concatenação dos subestados
							if not agrupa_estados(novos_estados) in estados:
								estados.append(agrupa_estados(novos_estados))

							# print("nova_regra_afd: "+str(nova_regra_afd))
							if nova_regra_afd != '' and not nova_regra_afd in regras_afd:
								regras_afd.append(nova_regra_afd)
							
							# print('novos_estados: '+str(novos_estados))
			
			# for regra in regras_afd:
			# 	print("regra_afd: "+ str(regra))
			# print(list_to_str(estados))

			# identificar estados finais
			finais: list = []
			for estado in estados:
				sub_estados: list = str(estado).split('-')
				for sub in sub_estados:
					if sub in afnd.get_estados_finais():
						finais.append(estado)
						break
					
			automato.set_estados(estados)
			automato.set_estados_finais(finais)
			automato.set_funcao_transicao(regras_afd)

			# print(str(automato.get_descricao()))
			# print(str(automato.get_alfabeto()))
			# print(str(automato.get_estado_inicial()))
			# print(str(automato.get_estados()))
			# print(str(automato.get_estados_finais()))
			# print(str(automato.get_funcao_transicao()))

			escreve_no_arquivo(automato.get_descricao(),automato.get_alfabeto(),automato.get_estados(),automato.get_estado_inicial(),automato.get_estados_finais(), automato.get_funcao_transicao())
			return automato

				


# 	def converteAFND(self, afn):
# 		automato = afd.AFD("","",False)
# 		automato.set_alfabeto(afn.get_alfabeto())
# 		automato.set_estado_inicial(afn.get_estado_inicial())
# 		automato.set_descricao("AFD Convertido com base no AFND: " + afn.get_descricao())

# 		estados: list = []
# 		estados.append(automato.get_estado_inicial())

# 		# converter estados
# 		for regra in afn.get_funcao_transicao():
# 			estado = regra[2]
# 			flag: bool = False
				
# 			flag = str(estado).replace('[', '').replace(']', '').replace('\'', '') in estados

# 			if flag:
# 				break
# 			else:
# 				estados.append(str(estado).replace('[', '').replace(']', '').replace('\'', ''))

# 		automato.set_estados(estados)

# 		# converter estados finais
# 		estados_finais: list = afn.get_estados_finais()
# 		finais_afn = afn.get_estados_finais()
# 		list_estados = list_to_str(estados).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').strip('q0').split("|")
# 		list_estados.remove('')
# 		list_estados.remove('')

# 		for estado in list_estados:
# 			sub_estados = estado.split(',')
# 			for sub in sub_estados:

# 				if sub in finais_afn:
# 					estados_finais.append(estado)

# 		print("Estados Finais:",estados_finais)
		

# 		automato.set_estados_finais(estados_finais)

# 		# converte funcao de transicao
# 		regras = []
# 		regras_afn = afn.get_funcao_transicao()

# 		for regra in regras_afn:
# 			for estado in list_estados:
# 				regra_afd = estado + " " + regra[1] + " "
# 				estados_regra = []
# 				sub_estados = estado.split(',')

# 				for sub in sub_estados:
# 					str_regra = str(regra[2]).replace('[', '').replace(']', '').replace('\'', '')
# 					estados_regra.append(str_regra)
			
# 				estados_regra = str(list(set(estados_regra)))
# 				estados_regra = str(estados_regra).replace('[', '').replace(']', '').replace('\'', '')
# 				regra_afd += estados_regra
# 				regras.append(regra_afd)

# 		nova_funcao_transicao = formata_funcao_transicao(regras)
# 		escreve_no_arquivo(automato.get_descricao(),automato.get_alfabeto(),automato.get_estados(),automato.get_estado_inicial(),automato.get_estados_finais(),nova_funcao_transicao)
# 		return

# 	def converteAFNE(self, afne: afne) -> None:
# 		# Setup inicial
# 		descricao: str = ("AFD Convertido com base no AFNE: " + afne.get_descricao())
# 		alfabeto: list = afne.get_alfabeto()
# 		estado_inicial: str = afne.get_estado_inicial()
# 		estados: list = afne.get_estados()
# 		estados_finais: list = afne.get_estados_finais()
# 		delta: list = []

# 		novos_estados: list = []

# 		#	Percorrer Função Transição AFNE
# 		regras_afne = afne.get_funcao_transicao()

# 		for regra in regras_afne:
# 			print("regra: "+ str(regra))

# 		for regra in regras_afne:
# 			for estado in estados:
# 				alfabeto = regra[1]
				
# 				# verificar se o estado atual esta nas regras do afne
# 				if estado == regra[0]:
# 					regra_afd = estado + " " + alfabeto + " "
# 					# print("Regra AFD:",regra_afd)
				
# 					estados_regra: list = []
# 					estados_regra = regra[2]

# 					sub_estados = estado.split(',')

# 					for sub in sub_estados:
# 						str_regra = str(estados_regra).replace('[', '').replace(']', '').replace('\'', '')
# 						estados_regra.append(str_regra)
			
# 					estados_regra = str(list(set(estados_regra)))
# 					estados_regra = str(estados_regra).replace('[', '').replace(']', '').replace('\'', '')
# 					regra_afd += estados_regra
# 					delta.append(regra_afd)
		
# 		for regra in delta:
# 			print("regra delta: " + str(regra))




# 		#	Finalização


# 		#	Estados Atualizado
# 		for est in novos_estados:
# 			estados.append(est)

# 		escreve_no_arquivo(descricao, alfabeto, estados, estado_inicial, estados_finais, delta)
# 		return

# """

# estados afd
# "q0" "[q0,q1]"

#  CONVERSÃO AFNE -> AFD

#   ["q1", "a", ["q0", "q2"]],
#   ["q1", "&", ["q2"],
#   ["q2", "&", ["q3"],
#   ["q3", "&", ["q5"]
#   ["q3", "b", ["q0", "q2"]],

#   ["q0", "q2"] => "qA"
#   e-fecho("q1") => ["q1", "q2", "q3", "q5"]
  
#   ["q1", "a", ["qA"]],
#   ["q1", "&", ["q1", "q2", "q3", "q5"]]


#   delta [0, 1, 2]
#   se ( len( atual[i][2]) > 1 ):
#       flag: bool = False
      
#       for estado in atual[i][2]:
#           flag = (estado in LISTA DE ESTADOS NOVOS)
      
#       if(flag):
#           #    Estado Novo ja foi feito
#           break
#       else:
#           #    PRECISA CRIAR UM NOVO ESTADO
# """