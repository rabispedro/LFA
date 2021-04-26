lista: list = ["q0", "q1", "q2"]
listadupla: list = [["q3"], ["q4"], ["q5", "q6"], ["q7", "q8", "q9"]]

print("Lista:",lista)
print("Lista Dupla:",listadupla)

novalista: list = []

for obj in lista:
	novalista.append(obj)

i: int = 0
while(i < len(listadupla)):
	for obj in listadupla[i]:
		novalista.append(obj)
	i += 1

print("Nova Lista:",novalista)

novalista = str(lista)
