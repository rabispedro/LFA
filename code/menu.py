import afd
import afnd
import afne
import conversor

def menu() -> None:
	automatos: list = []

	#	Inicialização dos Automatos
	afd_nome: str = "./testes.json"
	afd_exemplo: str = "exemplo_1"
	autobot: afd = afd.AFD(afd_nome, afd_exemplo, True)
	automatos.append(autobot)

	afnd_nome: str = "./afnd_data.json"
	afnd_exemplo: str = "exemplo_3"
	decepticon: afnd = afnd.AFND(afnd_nome, afnd_exemplo, True)
	automatos.append(decepticon)

	afne_nome: str = "./afne_data.json"
	afne_exemplo: str = "exemplo_1"
	robocop: afne = afne.AFNE(afne_nome, afne_exemplo, True)
	automatos.append(robocop)

	#	Escolha entre os Automatos
	print("Selecione o automato:")
	print("1) AFD")
	print("2) AFND")
	print("3) AFNE")
	print("4) Conversor AFND -> AFD")
	# print("5) Conversor AFNE -> AFD")
	opt: int = int(input("Opcao: "))
	print()
	if(opt == 1):
		print("AFD Selecionado")
	elif(opt == 2):
		print("AFND Selecionado")
	elif(opt == 3):
		print("AFNE Selecionado")
	elif(opt == 4):
		print("Conversor AFND -> AFD Secelionado")
	else:
		print("Servico Indisponível. ;(\n")
		return

	opt -= 1
	if(opt <= 2):
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
	elif(opt == 3):
		# print("Em obras...")
		automato = afnd.AFND(afnd_nome, afnd_exemplo, True)
		convert = conversor.Conversor()
		convert.converteAFND(automato)

		print("Saindo :(\n")
		return
	elif(opt == 4):
		print("Saindo :(\n")
		print("Em obras...")
		return

menu()