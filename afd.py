import ast

class AFD:
	_descricao: str = ""
	_alfabeto: list = []
	_estados: list = []
	_estado_inicial: str = ""
	_estados_finais: list = []
	_funcao_transicao: list = []

	def __init__(self, name: str, exemple: str, opt: bool) -> None:
		if(opt):
			exemplo: str = exemple
			filename: str = name

			arquivo: IO = open(filename, "r")
			conteudo: str = arquivo.read()
			json: dict = ast.literal_eval(conteudo)
			arquivo.close()

			self.set_descricao(json[exemplo]["descricao"])
			self.set_alfabeto(json[exemplo]["alfabeto"])
			self.set_estados(json[exemplo]["estados"])
			self.set_estado_inicial(json[exemplo]["estado_inicial"])
			self.set_estados_finais(json[exemplo]["estados_finais"])
			self.set_funcao_transicao(json[exemplo]["funcao_transicao"])
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
	def verifica_alfabeto(self, entrada: list) -> bool:
		flag: bool = False

		for i in entrada:
			flag = False
			for j in self.get_alfabeto():
				if (i == j):
					flag = True
			if (not flag):
				return flag
		return flag

	def verifica_estados(self, entrada: list, estado_atual: str, estados_finais: list) -> None:
		delta: list = self.get_funcao_transicao()

		if(self.eh_estado_morto(estado_atual)):
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
					self.verifica_estados(entrada[1:], delta[i][2][j],estados_finais)
					j += 1
			i += 1

	def verifica_cadeia(self, entrada: str) -> bool:
		if(len(entrada) == 0):
			return (self._estado_inicial in self._estados_finais)

		entrada_processada: list = entrada.split(" ")

		#	Verifica Alfabeto
		if(not self.verifica_alfabeto(entrada_processada)):
			print("\033[33mErro: Entrada não pertence ao alfabeto.\033[0;0m")
			return False
				
		#	Percorre Estados
		flag: bool = False
		estados_finais: list = []
		self.verifica_estados(entrada_processada, self.get_estado_inicial(), estados_finais)

		#	Verifica Estados Finais	
		for i in estados_finais:
			flag = False
			for j in self.get_estados_finais():
				if (i == j):
					flag = True
					return flag
		return flag

	def eh_estado_morto(self, estado: str) -> bool:
		tamanho_alfabeto: int = len(self.get_alfabeto())
		estados_com_autoinputs: list = self.tem_autoinput()
		eh_morto: bool = False

		if(estados_com_autoinputs.count(estado) == tamanho_alfabeto) and (estado not in self.get_estados_finais()):
			eh_morto = True

		return eh_morto
			
	# Retorna uma lista dos estados que tem autoinputs
	def tem_autoinput(self) -> list:
		estados: list = self.get_estados()
		delta: list = self.get_funcao_transicao()
		estados_com_autoinputs: list = []

		for transicoes in delta:
			if(transicoes[0] == transicoes[2][0]):
				estados_com_autoinputs.append(transicoes[0])
		return estados_com_autoinputs

	def tem_multiplos_estados(self) -> bool:
		delta: list = self.get_funcao_transicao()
		tamanho_estados: int = len(self.get_estados())
		tamanho_alfabeto: int = len(self.get_alfabeto())
		flag: bool  = False

		# verifica se algum estado recebe mais que len(Sigma) entradas
		if(len(delta) > tamanho_alfabeto*tamanho_estados):
			flag = True

		# verifica se tem mais que um próximo estado
		for transicoes in delta:
			if len(transicoes[2]) > 1:
				flag = True
		return flag