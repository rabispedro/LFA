"""
Automato Finito Não Deterministico
	Descricao: breve descrição opcional para informar sobre o AFND
	Estados: lista de estados pertencentes ao AFND
	Estado Inicial: estado inicial pertencente ao AFND
	Estados Finais: lista de estados finais pertencentes ao AFND
	Alfabeto: lista de caractere(s) pertencentes ao AFND
	Funcao Transicao: função para deslocamento de estados do AFND
	
	Exemplo:
		Descrição: Automato que reconhece números pares de 0's e 1's
		Estados: [q0, q1, q2, q3]
		Estado Inicial: q0
		Estados Finais: [q0]
		Alfabeto: [0, 1]
		Funcao Transicao: [
			[q0, 0, [q1]],
			[q0, 1, [q3]],
			[q1, 0, [q0]],
			[q1, 1, [q2]],
			[q2, 0, [q3]],
			[q2, 1, [q1]],
			[q3, 0, [q2]],
			[q3, 0, [q0]]
		]
"""

class AFND:
	_descricao: str = ""
	_alfabeto: list = []
	_estados: list = []
	_estado_inicial: str = ""
	_estados_finais: list = []
	_funcao_transicao: list = []

	def __init__(self) -> None:
		"""
		filename: arquivo
		setters & getters
		"""
		return
	
	def get_descricao(self) -> str:
		return self._descricao
	
	def set_descricao(self, descricao: str) -> None:
		self._descricao = descricao
		return

	def get_alfabeto(self) -> str:
		return self._alfabeto

	def set_alfabeto(self, alfabeto: str) -> None:
		self._alfabeto = alfabeto
		return

	def get_estados(self) -> list:
		return self._estados

	def set_estados(self, estados: list) -> None:
		self._estados = estados
		return
	
	def get_estado_inicial(self) -> str:
		return self._estado_inicial

	def set_estado_inicial(self, estado_inicial: str) -> None:
		self._estado_inicial = estado_inicial
		return
	
	def get_estados_finais(self) -> list:
		return self._estados_finais

	def set_estados_finais(self, estados_finais: list) -> None:
		self._estados_finais = estados_finais
		return

	def get_funcao_transicao(self) -> list:
		return self._funcao_transicao
	
	def set_funcao_transicao(self, funcao_transicao: list) -> None:
		self._funcao_transicao = funcao_transicao
		return

	def show(self) -> None:
		print("AUTOMATO FINITO NÃO DETERMINISTICO\n")
		print("Tipo:",type(self))
		print("Descricao:",self._descricao)
		print("Alfabeto:",self._alfabeto)
		print("Estados:",self._estados)
		print("Estado inicial:",self._estado_inicial)
		print("Estado Finais:",self._estados_finais)
		print("Funcao Transicao:")

		i: int = 0 
		while (i < len(self._funcao_transicao)):
			print("[",self._funcao_transicao[i][0],"]",end="")
			print("----[",self._funcao_transicao[i][1],"]---->",end="")
			print(self._funcao_transicao[i][2])
			i += 1
		print()

		return

def verifica_alfabeto(automato: AFND, entrada: list) -> bool:
	flag: bool = False
	print("Verificando alfabeto:")
	print("Alfabeto:",automato.get_alfabeto())
	print("Entrada:",entrada)

	for i in entrada:
		flag = False
		for j in automato.get_alfabeto():
			if (i == j):
				flag = True
		if (not flag):
			return flag
	return flag

def verifica_estados(automato: AFND, entrada: list, estado_atual: str, estados_finais: list) -> list:
	if(entrada == []):
		estados_finais.append(estado_atual)
		print("Fim:",estados_finais)
		return estados_finais
	
	entrada_atual: str = entrada[0]
	delta: list = automato.get_funcao_transicao()

	print("Entrada:",entrada)
	print("Nova entrada:",entrada[1:])

	i: int = 0
	while (i < len(delta)):
		if((estado_atual == delta[i][0]) and (entrada_atual == delta[i][1])):
			#	Estado encontrado e entrada encontrada
			print("Estado atual:",estado_atual)
			print("Entrada atual: ",entrada_atual)
			print("Próximo(s) estado(s):",delta[i][2])
			j: int = 0
			while( j < len(delta[i][2])):
				# estados_finais.append(delta[i][2][j])
				print("<---",(verifica_estados(automato, entrada[1:],delta[i][2][j], estados_finais)))
				# estados_finais.append(verifica_estados(automato, entrada[1:],delta[i][2][j], estados_finais))
				j += 1
		i += 1

	return estados_finais
	

def verifica_cadeia(automato: AFND, entrada: str) -> bool:
	entrada_processada: list = entrada.split(" ")
	print("Entrada processada:",entrada_processada)

	#	Verifica Alfabeto
	if(not verifica_alfabeto(automato, entrada_processada)):
		print("Erro: Entrada não pertence ao alfabeto.")
		return False
			
	#	Percorre Estados
	flag: bool = False
	estados_finais: list = verifica_estados(automato, entrada_processada, automato.get_estado_inicial(), [])

	print("Estados Finais:",estados_finais)
	print("Estados Finais Automato:",automato.get_estados_finais())

	#	Verifica Estados Finais
	for i in estados_finais:
		flag = False
		for j in automato.get_estados_finais():
			if (i == j):
				flag = True
				return flag
		return flag

def menu() -> None:
	automato: AFND = AFND()
	automato.set_descricao("Automato que reconhece números pares de 0's e 1's")
	automato.set_alfabeto(["0", "1"])
	automato.set_estados(["q0", "q1", "q2", "q3"])
	automato.set_estado_inicial("q0")
	automato.set_estados_finais(["q0"])
	automato.set_funcao_transicao([
		["q0", "0", ["q1"]],
		["q0", "1", ["q3"]],
		["q1", "0", ["q0"]],
		["q1", "1", ["q2"]],
		["q2", "0", ["q3"]],
		["q2", "1", ["q1"]],
		["q3", "0", ["q2"]],
		["q3", "0", ["q0"]]
	])
	automato.show()

	while (True):
		entrada: str = input("Digite uma entrada (separe os simbolos por espaços ou digite \"sair\"): ")
		if (entrada == "sair"):
			break

		if(verifica_cadeia(automato, entrada)):
			print("CADEIA ACEITA!!!\n")
		else:
			print("CADEIA REJEITADA!!!\n")
	
	print("Saindo :(\n")
	return

menu()