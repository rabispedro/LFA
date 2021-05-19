import ast

class AFND:
	_descricao: str = ""
	_alfabeto: list = []
	_estados: list = []
	_estado_inicial: str = ""
	_estados_finais: list = []
	_funcao_transicao: list = []
	_cadeia_vazia :str = "&"

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

	def get_cadeia_vazia(self) -> str:
		return self._cadeia_vazia
	
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
		if(entrada == []):
			estados_finais.append(estado_atual)
			return

		entrada_atual: str = entrada[0]
		delta: list = self.get_funcao_transicao()
		i: int = 0
		novos_estados_finais: list = []

		#	Verificando se o estado tem transição
		flag: bool = False
		while(i < len(delta)):
			if(estado_atual == delta[i][0]):
				flag = True
				break
			i += 1
			
		if(flag):

			i = 0
			while (i < len(delta)):
				if((estado_atual == delta[i][0]) and ((entrada_atual == delta[i][1]) or (self.get_cadeia_vazia() == delta[i][1]))):
					#	Estado encontrado e entrada encontrada (ou cadeia vazia)

					print("[",estado_atual,"]",end="")
					print("----[",entrada_atual,"]---->",delta[i][2])
					j: int = 0
					
					#	Testar TODAS as possibilidades
					while( j < len(delta[i][2])):
						self.verifica_estados(entrada[1:], delta[i][2][j],estados_finais)
						j += 1
				i += 1
		else:
			estados_finais.append(estado_atual)

		return

	def verifica_cadeia(self, entrada: str) -> bool:
		if(len(entrada) == 0):
			return (self._estado_inicial in self._estados_finais)

		entrada_processada: list = entrada.split(" ")

		#	Verifica Alfabeto
		if(not self.verifica_alfabeto(entrada_processada)):
			print("Erro: Entrada não pertence ao alfabeto.")
			return False
				
		#	Percorre Estados
		flag: bool = False
		estados_finais: list = []
		self.verifica_estados(entrada_processada, self.get_estado_inicial(), estados_finais)
		print("Estados Alcançados:",estados_finais)

		#	Verifica Estados Finais	
		for i in estados_finais:
			flag = False
			for j in self.get_estados_finais():
				if (i == j):
					flag = True
					return flag
		return flag
