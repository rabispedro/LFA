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
			teste: list = []
			teste = self.e_fecho(estado_atual)
			estados_finais.append(teste)
			print("Teste:",teste)
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
						auxiliar_fecho(estado_atual, estados_encontrados)
					j += 1
				break
			i += 1

			return

		"""
		Guardar efechos atingidos + [proximos efechos]
        Caso Base: não há proximos estados -> gravar estado atual
        ["q1", "q2", "q3", ...]

        efecho (q1) = q1 + efecho (q2) = q1 + q2 + efecho(q3) ...
        10! = 10 * 9! = 10 * 9 * 8! = 10 * 9 * 8 * 7! ...
        



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