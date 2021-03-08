#include<iostream>
#include<vector>
#include<map>
#include<utility>
#include<cassert>

using namespace std;

void test();
string extractStringBetweenTags(string stringToSearch="", string startTag="", string endTag="");
vector<string> vectorizeSpacedString(string str="");
string switchCommaToSpace(string str="");

class AFN;

/*	ATRIBUTOS GERAIS DE UM AUTOMATO
*	Estado Inicial <String>: estado por onde se inicia um automato.
*	Estados Finais <Vetor de String>: conjunto de estados aceitos pelo automato.
*	Estados <Vector de String>: conjunto de estados pertencentes ao automato.
*	Alfabeto <Vector de String>: conjunto de simbolos que pertencem ao automato.
*	Função de Transição <Map de Vector de Pair de String,String>: conjunto de regras de interação entre os estados de um automato.
*	Leitura de arquivo: ler arquivos e configurar o automato com base neste.
*	
*	----------------------------------------------------------------------------
*	
*	INTERPRETAÇÃO (pertence ao alfabeto)
*	{"a", "b", "c"}
*	{"ALFA", "BETA", "GAMA"}
*	
*	"abc" -> ERRADO
*	"a b c" -> CERTO
*	"ALFABETAGAMA" -> ERRADO
*	"ALFA BETA GAMA" -> CERTO
*
*	----------------------------------------------------------------------------
*	
*	LEITURA DO ARQUIVO
*	Uso de TAGS: [TAG]...[-TAG]
*	Chamada de setters.
*	
*	Função de Transição:
*	q0 a q1
*	q0 b q2
*	q1 b q2
*	q2 c q3
*	q3 d q0
*	q3 e q1
*	
*		Guardar o estado atual e o ultimo estado;
*		Preencher o vector do estado atual;
*		Ao chegar a um estado atual diferente do ultimo estado, setFuncaoTransicao(string, vector)
*	
*	DEMONSTRAÇÃO DA ESTRUTURA: FUNÇÕES DE TRANSIÇÃO
*	MAP <first, second>
*	VECTOR[index] = value
*	PAIR <first, second>
*	
*	[q0]
*		|---"a"--->[q1]
*		|---"b"--->[q2]
*	[q1]
*		|---"b"--->[q2]
*	[q2]
*		|---"c"--->[q3]
*	[q3]
*		|---"d"--->[q0]
*		|---"e"--->[q1]
*	
*	map<string, vector<pair<string, string>>>
*	------------------------------------------
*	q0 => ("a"|"q1") -> ("b"|"q2")
*	------------------------------------------
*	q0 -> index[0] = ("a"|"q1")
*	q0 -> index[1] = ("b"|"q2") 
*	------------------------------------------
*	q0 -> index[0].first = "a"
*	q0 -> index[0].second = "q1"
*	q0 -> index[1].first = "b"
*	q0 -> index[2].second = "q2"
*/




/*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*	
*/

int main(){
	test();

	
	cout<<"Finished!\n";
	return 0;
}

vector<string> vectorizeSpacedString(string str){
			string state;
			vector<string> aux;
			for(int i=0; i<str.size(); i++){
				if(str[i] == ' '){
					aux.push_back(state);
					state.clear();
				}else{
					state += str[i];
				}
			}
			aux.push_back(state);
			state.clear();
			return aux;
}

string switchCommaToSpace(string str){
	string temp;
	for(int i=0; i<str.size(); i++){
		if(str.at(i) == ','){
			temp += ' ';
		}else{
			temp += str.at(i);
		}
	}
	return temp;
}

string extractStringBetweenTags(string stringToSearch, string startTag, string endTag){
	int start = startTag.size();
	int count = (stringToSearch.size() - (startTag.size() + endTag.size()));

	return stringToSearch.substr(start, count);
}

class AFN{

};

void test(){
	//	Vetoriza uma string com espaços
	assert(vectorizeSpacedString() == vector<string>({""}));
	assert(vectorizeSpacedString("") == vector<string>({""}));
	assert(vectorizeSpacedString("q0 q1") == vector<string>({"q0", "q1"}));

	//	Troca viruglas (",") por espaços (" ")
	assert(switchCommaToSpace() == "");
	assert(switchCommaToSpace("") == "");
	assert(switchCommaToSpace(",") == " ");
	assert(switchCommaToSpace("q0,") == "q0 ");
	assert(switchCommaToSpace("q0,q1") == "q0 q1");

	//	Retira TAGS de uma string
	assert(extractStringBetweenTags() == "");
	assert(extractStringBetweenTags("") == "");
	assert(extractStringBetweenTags("", "") == "");
	assert(extractStringBetweenTags("", "", "") == "");
	assert(extractStringBetweenTags("[TAG]Uma frase de teste.[-TAG]", "[TAG]", "[-TAG]") == "Uma frase de teste.");
}