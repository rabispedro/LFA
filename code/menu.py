import afd
import afnd

def menu() -> None:
	automatos: list = []

	#	Inicialização dos Automatos
	afd_nome: str = "./afd_data.json"
	afd_exemplo: str = "exemplo_2"
	autobot: afd = afd.AFD(afd_nome, afd_exemplo, True)
	automatos.append(autobot)

	afnd_nome: str = "./afnd_data.json"
	afnd_exemplo: str = "exemplo_3"
	decepticon: afnd = afnd.AFND(afnd_nome, afnd_exemplo, True)
	automatos.append(decepticon)

	#	Escolha entre os Automatos
	print("Selecione o automato:")
	print("1) AFD")
	print("2) AFND")
	print()
	opt: int = int(input("Opcao: "))
	if(opt == 1):
			print("AFD Selecionado");
	elif(opt == 2):
			print("AFND Selecionado");

	opt -= 1

	#	DEBUG
	"""
	print("Lista de automatos")
	aux: int = 0
	for i in automatos:
		print("[",aux,"]:",i)
		aux += 1
	"""


	automatos[opt].show()
	print()

	while (True):
		entrada: str = input("Digite uma entrada (separe os simbolos por espaços ou digite \"sair\"): ")
		if (entrada.lower() == "sair"):
			break

		if(automatos[opt].verifica_cadeia(entrada)):
			print("CADEIA ACEITA!!!\n")
		else:
			print("CADEIA REJEITADA!!!\n")		
		print("="*128)
	
	print("Saindo :(\n")
	return

menu()