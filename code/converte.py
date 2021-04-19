import afd
import afnd
# import afne

# coloca parenteses em todos os estados
def encapsula_estados(afn):
	nova_funcao_transicao = afn.get_funcao_transicao()
	lista_interna = []

	for transicao in nova_funcao_transicao:
		transicao[0] = [transicao[0]]

	return nova_funcao_transicao

def conversao_automatos(afn):
	automato: afd = afd.AFD("","", False)
	automato.set_descricao(afn.get_descricao())
	automato.set_alfabeto(afn.get_alfabeto())
	automato.set_estado_inicial(afn.get_estado_inicial())

	# estados que sao atingidos ja contados por ex( "q0,q1" )
	estados: list = []

	# numero do proximo estado a ser criado
	num_atual: int = len(afn.get_estados())


	# for obj in afn.get_funcao_transicao():
	# 		if(len(obj[2]) > 1):
	# 			if(not obj[2] in estados):
	# 				estados.append(obj[2])
	# 				automato.set_estado("q"+ num_atual)
	# 				# É PRA FAZER UM ESTADO NOVO
	# 			automato.set_transicao(obj[0], obj[1], "q"+num_atual)
	# 		automato.set_transicao(obj[0], obj[1], obj[2])
	


afnd_nome: str = "./afnd_data.json"
afnd_exemplo: str = "exemplo_3"
decepticon: afnd = afnd.AFND(afnd_nome, afnd_exemplo, True)

print(encapsula_estados(decepticon))
conversao_automatos(decepticon)