"""
Automato Finito Deterministico
	Descricao: breve descrição opcional para informar sobre o AFD
	Estados: lista de estados pertencentes ao AFD
	Estado Inicial: estado inicial pertencente ao AFD
	Estados Finais: lista de estados finais pertencentes ao AFD
	Alfabeto: lista de caractere(s) pertencentes ao AFD
	Funcao Transicao: função para deslocamento de estados do AFD
	
	Exemplo:
		Descrição: Automato que reconhece todas as cadeias que começam com 0
		Estados: [q0, q1, q2]
		Estado Inicial: q0
		Estados Finais: [q1]
		Alfabeto: [0, 1]
		Funcao Transicao: [
			[q0, 0, [q1]],
			[q0, 1, [q2]],
			[q1, 0, [q1]],
			[q1, 1, [q1]],
			[q2, 0, [q2]],
			[q2, 1, [q2]],
		]
"""

class AFD:
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
		print("AUTOMATO FINITO DETERMINISTICO\n")
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
		print("="*128,"\n")

		return


# Verifica se as entradas fazem parte do alfabeto
def verifica_alfabeto(automato: AFD, entrada: list) -> bool:

	flag: bool = False

	for i in entrada:
		flag = False
		for j in automato.get_alfabeto():
			if (i == j):
				flag = True
		if (not flag):
			return flag
	return flag


def verifica_estados(automato: AFD, entrada: list, estado_atual: str, estados_finais: list) -> None:

	delta: list = automato.get_funcao_transicao()

	if(eh_estado_morto(estado_atual,automato)):
		proximo_estado: list = [estado_atual]

		for entrada_atual in entrada:
			print("[",estado_atual,"]",end="")	
			print("----[",entrada_atual,"]---->",proximo_estado)		
		estados_finais = []
		return
	

	if(entrada == []):
		estados_finais.append(estado_atual)
		return

	entrada_atual: str = entrada[0]

	i: int = 0
	while (i < len(delta)):
		if((estado_atual == delta[i][0]) and (entrada_atual == delta[i][1])):
			#	Estado encontrado e entrada encontrada
			print("[",estado_atual,"]",end="")
			print("----[",entrada_atual,"]---->",delta[i][2])

			j: int = 0
			while( j < len(delta[i][2])):
				verifica_estados(automato, entrada[1:], delta[i][2][j],estados_finais)
				j += 1
		i += 1


def verifica_cadeia(automato: AFD, entrada: str) -> bool:
	
	entrada_processada: list = entrada.split(" ")

	#	Verifica Alfabeto
	if(not verifica_alfabeto(automato, entrada_processada)):
		print("Erro: Entrada não pertence ao alfabeto.")
		return False
			
	#	Percorre Estados
	flag: bool = False
	estados_finais: list = []
	verifica_estados(automato, entrada_processada, automato.get_estado_inicial(), estados_finais)

	#	Verifica Estados Finais
	if(estados_finais[0] in automato.get_estados_finais()):
	 	flag = True
	return flag

def eh_estado_morto(estado: str, automato: AFD) -> bool:
	
	tamanho_alfabeto: int = len(automato.get_alfabeto())
	estados_com_autoinputs: list = tem_autoinput(automato)
	eh_morto: bool = False

	if(estados_com_autoinputs.count(estado) == tamanho_alfabeto) and (estado not in automato.get_estados_finais()):
		eh_morto = True

	return eh_morto
		

def tem_autoinput(automato: AFD) -> list:
	estados: list = automato.get_estados()
	delta: list = automato.get_funcao_transicao()
	estados_com_autoinputs: list = []

	for transicoes in delta:
		if(transicoes[0] == transicoes[2][0]):
			estados_com_autoinputs.append(transicoes[0])
	return estados_com_autoinputs

def tem_multiplos_estados(automato: AFD) -> bool:

	delta: list = automato.get_funcao_transicao()
	tamanho_estados: int = len(automato.get_estados())
	tamanho_alfabeto: int = len(automato.get_alfabeto())
	flag: bool  = False

	# verifica se algum estado recebe mais que len(Sigma) entradas
	if(len(delta) > tamanho_alfabeto*tamanho_estados):
		flag = True

	# verifica se tem mais que um próximo estado
	for transicoes in delta:
		if len(transicoes[2]) > 1:
			flag = True
	return flag

def menu() -> None:
	autobot0: AFD = AFD()
	autobot0.set_descricao("Automato que reconhece números pares de 0's e 1's")
	autobot0.set_alfabeto(["0", "1"])
	autobot0.set_estados(["q0", "q1", "q2", "q3"])
	autobot0.set_estado_inicial("q0")
	autobot0.set_estados_finais(["q0"])
	autobot0.set_funcao_transicao([
		["q0", "0", ["q1"]],
		["q0", "1", ["q3"]],
		["q1", "0", ["q0"]],
		["q1", "1", ["q2"]],
		["q2", "0", ["q3"]],
		["q2", "1", ["q1"]],
		["q3", "0", ["q2"]],
		["q3", "1", ["q0"]]
	])
	# autobot0.show()	

	autobot1: AFD = AFD()
	autobot1.set_descricao("Automato que reconhece cadeias que começam em 0")
	autobot1.set_alfabeto(["0", "1"])
	autobot1.set_estados(["q0", "q1", "q2"])
	autobot1.set_estado_inicial("q0")
	autobot1.set_estados_finais(["q1"])
	autobot1.set_funcao_transicao([
		["q0", "0", ["q1"]],
		["q0", "1", ["q2"]],
		["q1", "0", ["q1"]],
		["q1", "1", ["q1"]],
		["q2", "0", ["q2"]],
		["q2", "1", ["q2"]]
	])
	#autobot1.show()

	autobot2: AFD = AFD()
	autobot2.set_descricao("Automato que reconhece cadeias que começam em 1 e terminam em 0")
	autobot2.set_alfabeto(["0", "1"])
	autobot2.set_estados(["q0", "q1", "q2"])
	autobot2.set_estado_inicial("q0")
	autobot2.set_estados_finais(["q2"])
	autobot2.set_funcao_transicao([
		["q0", "1", ["q1"]],
		["q0", "0", ["q0"]],
		["q1", "1", ["q1"]],
		["q1", "0", ["q2"]],
		["q2", "0", ["q2"]],
		["q2", "1", ["q1"]]
	])
	# autobot2.show()

	autobot3: AFD = AFD()
	autobot3.set_descricao("Automato que reconhece cadeias que possuem tres 0's consecutivos")
	autobot3.set_alfabeto(["0", "1"])
	autobot3.set_estados(["q0", "q1", "q2", "q3"])
	autobot3.set_estado_inicial("q0")
	autobot3.set_estados_finais(["q1","q2","q3"])
	autobot3.set_funcao_transicao([
		["q0", "1", ["q0"]],
		["q0", "0", ["q1"]],
		["q1", "1", ["q1"]],
		["q1", "0", ["q2"]],
		["q2", "1", ["q2"]],
		["q2", "0", ["q3"]],
		["q3", "0", ["q1"]],
		["q3", "1", ["q3"]]
	])
	# autobot3.show()

	autobot4: AFD = AFD()
	autobot4.set_descricao("Automato que reconhece cadeias que possuem 01 em algum lugar")
	autobot4.set_alfabeto(["0", "1"])
	autobot4.set_estados(["q0", "q1", "q2"])
	autobot4.set_estado_inicial("q0")
	autobot4.set_estados_finais(["q2"])
	autobot4.set_funcao_transicao([
		["q0", "1", ["q0"]],
		["q0", "0", ["q1"]],
		["q1", "1", ["q2"]],
		["q1", "0", ["q1"]],
		["q2", "1", ["q2"]],
		["q2", "0", ["q2"]],
	])
	
	# autobot4.show()

	autobot5: AFD = AFD()
	autobot5.set_descricao("Automato que reconhece cadeias que terminam com 100")
	autobot5.set_alfabeto(["0", "1"])
	autobot5.set_estados(["q0", "q1", "q2", "q3"])
	autobot5.set_estado_inicial("q0")
	autobot5.set_estados_finais(["q3"])
	autobot5.set_funcao_transicao([
		["q0", "1", ["q1"]],
		["q0", "0", ["q0"]],
		["q1", "1", ["q1"]],
		["q1", "0", ["q2"]],
		["q2", "1", ["q1"]],
		["q2", "0", ["q3"]],
		["q3", "1", ["q1"]],
		["q3", "0", ["q0"]],
	])
	
	autobot5.show()

	print()

	while (True):
		entrada: str = input("Digite uma entrada (separe os simbolos por espaços ou digite \"sair\"): ")
		if (entrada.lower() == "sair"):
			break
		
		if(tem_multiplos_estados(autobot5)):
			print("AFD NAO POSSUI MULTIPLOS PROXIMOS ESTADOS\n")
		else:
			if(verifica_cadeia(autobot5, entrada)):
				print("CADEIA ACEITA!!!\n")
			else:
				print("CADEIA REJEITADA!!!\n")		
		print("="*128)
	
	print("Saindo :(\n")
	return

menu()