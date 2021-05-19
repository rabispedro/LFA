import ast

class AFNE:
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
		print("AUTOMATO FINITO NÃO DETERMINISTICO COM E-FECHO\n")
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
			e_fecho_atual: list = []
			e_fecho_atual = self.e_fecho(estado_atual)

			for obj in e_fecho_atual:				
				estados_finais.append(obj)			
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
					#	Verificando se encontrou a EPSILON ou ENTRADA NORMAL
					if(delta[i][1] == self.get_cadeia_vazia()):
						print("----[",self.get_cadeia_vazia(),"]---->",delta[i][2])
					else:
						print("----[",entrada_atual,"]---->",delta[i][2])
					j: int = 0
					
					#	Utilizar o E-fecho
					if(delta[i][1] == self.get_cadeia_vazia()):
						# "q0", "&", ["q1", "q2"]

						temp: list = []
						for obj in delta[i][2]:
							#	Pegando o e_fecho de cada estado resultante
							temp = self.e_fecho(obj)
							lista_efecho: list = []
							
							#	Formatando a lista para ser uma lista de strings
							for est in temp:
								lista_efecho.append(est)
							
							# ["q1", "q2", "q4"]

							for estado in lista_efecho:
								self.verifica_estados(entrada, estado, estados_finais)

					else:
						#	Entrada NORMAL
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
			print ("Estados Alcançados:", self.get_estado_inicial())
			fecho: list = self.e_fecho(self.get_estado_inicial())
			estados_finais: list = []
			
			for obj in fecho:
				estados_finais.append(obj)
			flag: bool = False
			
			for obj in estados_finais:
				if obj in self.get_estados_finais():
					flag = True
					return flag			
			return flag

		entrada_processada: list = entrada.split(" ")
										
		#	Verifica Alfabeto
		if(not self.verifica_alfabeto(entrada_processada)):
			print("Erro: Entrada não pertence ao alfabeto.")
			return False
				
		#	Percorre Estados
		flag: bool = False
		estados_finais: list = []
		self.verifica_estados(entrada_processada, self.get_estado_inicial(), estados_finais)
		estados_finais = list(set(estados_finais))
		print("Estados Alcançados:",estados_finais)
		

#    Adicionando efechos na lista de estados finais
		temp: list = []
		novos_estados_finais: list = []

		#    Ajustar a lista de e_fecho corretamente
		for i in estados_finais:
			temp = self.e_fecho(i)
			for j in temp:
				novos_estados_finais.append(j)
		
		#    Inserir e_fechos ajustados à lista de estados finais original
		for i in novos_estados_finais:
			estados_finais.append(i)

		#    Otimiza a lista de estados finais
		estados_finais = list(set(estados_finais))
		

		print('****',estados_finais,'****')
		#    Verifica estados finais (COM e_fechos() previamente inseridos)
		for i in estados_finais:
			flag = False
			for j in self.get_estados_finais():
				if(i == j):
					flag = True
					return flag
		return flag

	# printa o estado e seus e-fechos
	def e_fecho(self, estado_atual: str) -> list:
		estados_finais: list = []
		self.auxiliar_fecho(estado_atual, estados_finais)
		
		print("[",estado_atual,"] E-Fecho:",estados_finais)
		return estados_finais


	def auxiliar_fecho(self, estado_atual: str, estados_encontrados: list) -> None:
		if(not (estado_atual in estados_encontrados)):
			estados_encontrados.append(estado_atual)

		delta: list = []
		delta = self.get_funcao_transicao()
		i: int = 0

		while(i < len(delta)):
			#	Verifica se estado atual possui transição vazia
			if((estado_atual == delta[i][0]) and (self.get_cadeia_vazia() == delta[i][1])):
				j: int = 0

				while(j < len(delta[i][2])):
					estado_atual = delta[i][2][j]
					if(not (estado_atual in estados_encontrados)):
						self.auxiliar_fecho(estado_atual, estados_encontrados)
					j += 1
				break
			i += 1
		return		