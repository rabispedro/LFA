#include<iostream>
#include<vector>
#include<map>
#include<utility>

using namespace std;

class Automata{
	private:
		vector<string> m_Estados;

		string m_EstadoInicial;
		vector<string> m_EstadosFinais;

		vector<string> m_Alfabeto;

		map<string,vector<pair<string,string>>> m_FuncaoTransicao;
	public:
		Automata(string filename){
			cout<<"File: "<<filename<<"\n";
		}

		void setEstados(vector<string> estados){
			m_Estados.clear();
			for(int i=0; i<estados.size(); i++){
				m_Estados.push_back(estados.at(i));
			}
		}

		vector<string> getEstados(){
			return m_Estados;
		}

		void setEstadoInicial(string estadoInicial){
			m_EstadoInicial = estadoInicial;
		}

		string getEstadoInicial(){
			return m_EstadoInicial;
		}


		void setEstadosFinais(vector<string> estadosFinais){
			m_EstadosFinais.clear();
			for(int i=0; i<estadosFinais.size(); i++){
				m_EstadosFinais.push_back(estadosFinais.at(i));
			}
		}

		vector<string> getEstadosFinais(){
			return m_EstadosFinais;
		}

		void setAlfabeto(vector<string> alfabeto){
			m_Alfabeto.clear();
			for(int i=0; i<alfabeto.size(); i++){
				m_Alfabeto.push_back(alfabeto.at(i));
			}
		}

		vector<string> getAlfabeto(){
			return m_Alfabeto;
		}

		// map<string,vector<pair<string,string>>> m_FuncaoTransicao;
		void setFuncaoTransicao(string estadoAtual, vector<pair<string,string>> vecAtual){
			m_FuncaoTransicao.insert(pair<string,vector<pair<string,string>>>(estadoAtual,vecAtual));
		}

		map<string,vector<pair<string,string>>> getFuncaoTransicao(){
			return m_FuncaoTransicao;
		}

		void addVec(string estadoAtual, pair<string,string>parAtual, vector<pair<string,string>>* vecAtual){
			// vector<pair<string,string>> vecPar;
			// vecPar.push_back(pair<string,string>("a","q1"));
			// vecPar.push_back(pair<string,string>("b","q2"));
			// funcaoTransicao.insert(pair<string,vector<pair<string,string>>>("q0",vecPar));
			// vecPar.clear();
			vecAtual->push_back(parAtual);
		}

		void resetFuncaoTransicao(){
			m_FuncaoTransicao.clear();
		}

		bool verificaCadeia(vector<string> entrada);

		string extractStringBetweenTags(string stringToSearch, string startTag, string endTag){
			int start = startTag.size();
			int count = (stringToSearch.size() - (startTag.size() + endTag.size()));

			return stringToSearch.substr(start, count);
		}

		void show(){
			cout<<"SHOW\n\n";

			//	Estados
			cout<<"Estados: ";
			for(int i=0; i<m_Estados.size(); i++){
				cout<<"["<<m_Estados.at(i)<<"] ";
			}
			cout<<"\n";

			//	Estado Inicial
			cout<<"Estado Inicial: ["<<m_EstadoInicial<<"]\n";

			//	Estados Finais
			cout<<"Estado(s) Final(is): ";
			for(int i=0; i<m_EstadosFinais.size(); i++){
				cout<<"["<<m_EstadosFinais.at(i)<<"] ";
			}
			cout<<"\n";

			//	Alfabeto
			cout<<"Alfabeto: {";
			for(int i=0; i<m_Alfabeto.size(); i++){
				if(i == (m_Alfabeto.size()-1)){
					cout<<m_Alfabeto.at(i)<<"";
				}else{
					cout<<m_Alfabeto.at(i)<<", ";
				}
			}
			cout<<"}\n";

			//	Função Transição
			cout<<"Funcao Transicao:\n";
			for(auto it : m_FuncaoTransicao){
				cout<<"\t["<<it.first<<"]\n";
				for(int i=0; i<it.second.size();i++){
					cout<<"\t  |---"<<it.second.at(i).first<<"--->["<<it.second.at(i).second<<"]\n";
		}
	}
	cout<<"\n";

		}
}typedef AFD;

/*	ATRIBUTOS GERAIS DE UM AUTOMATO
*	Estado Inicial: estado por onde se inicia um automato.
*	Estados Finais: conjunto de estados aceitos pelo automato.
*	Estados: conjunto de estados pertencentes ao automato.
*	Alfabeto: conjunto de simbolos que pertencem ao automato.
*	Função de Transição: conjunto de regras de interação entre os estados de um automato.
*	Leitura de arquivo: ler arquivos e configurar o automato com base neste.
*	
*/

/*	INTERPRETAÇÃO (pertence ao alfabeto)
*	{"a", "b", "c"}
*	{"ALFA", "BETA", "GAMA"}
*	
*	"abc" -> ERRADO
*	"a b c" -> CERTO
*	"ALFABETAGAMA" -> ERRADO
*	"ALFA BETA GAMA" -> CERTO
*/

int main(){
	AFD autobot("afd.txt");

	//	Teste inserindo estados
	vector<string> estados;
	estados.push_back("q0");
	estados.push_back("q1");
	estados.push_back("q2");
	estados.push_back("q3");
	autobot.setEstados(estados);

	//	Teste inserindo estado inicial
	autobot.setEstadoInicial(estados.at(0));
	
	//	Teste inserindo estados finais
	vector<string> estadosFinais;
	estadosFinais.push_back(estados.at(2));
	estadosFinais.push_back(estados.at(3));
	autobot.setEstadosFinais(estadosFinais);

	//	Teste inserindo alfabeto
	vector<string> alfabeto;
	alfabeto.push_back("a");
	alfabeto.push_back("b");
	alfabeto.push_back("c");
	alfabeto.push_back("d");
	alfabeto.push_back("e");
	autobot.setAlfabeto(alfabeto);

	//	Teste inserindo funcao transicao
	map<string,vector<pair<string,string>>> funcaoTransicao;
	vector<pair<string,string>> vecPar;
	vecPar.push_back(pair<string,string>("a","q1"));
	vecPar.push_back(pair<string,string>("b","q2"));
	funcaoTransicao.insert(pair<string,vector<pair<string,string>>>("q0",vecPar));
	vecPar.clear();
	vecPar.push_back(pair<string,string>("b","q2"));
	funcaoTransicao.insert(pair<string,vector<pair<string,string>>>("q1",vecPar));
	vecPar.clear();
	vecPar.push_back(pair<string,string>("c","q3"));
	funcaoTransicao.insert(pair<string,vector<pair<string,string>>>("q2",vecPar));
	vecPar.clear();
	vecPar.push_back(pair<string,string>("d","q0"));
	vecPar.push_back(pair<string,string>("e","q1"));
	funcaoTransicao.insert(pair<string,vector<pair<string,string>>>("q3",vecPar));

	// autobot.setFuncaoTransicao("q0",pair<string,string>("a","q1"));
	// autobot.setFuncaoTransicao("q0",pair<string,string>("b","q2"));
	// autobot.setFuncaoTransicao("q1",pair<string,string>("b","q2"));
	// autobot.setFuncaoTransicao("q2",pair<string,string>("c","q3"));
	// autobot.setFuncaoTransicao("q3",pair<string,string>("d","q0"));
	// autobot.setFuncaoTransicao("q3",pair<string,string>("e","q1"));

	// cout<<"FUNCAO TRANSICAO:\n";
	// for(auto it : funcaoTransicao){
	// 	cout<<"\t["<<it.first<<"]\n";
	// 	for(int i=0; i<it.second.size();i++){
	// 		cout<<"\t  |---"<<it.second.at(i).first<<"--->["<<it.second.at(i).second<<"]\n";
	// 	}
	// }
	// cout<<"\n";

	//	Relacionado a leitura do arquivo e setter da Função Transição
	vector<pair<string,string>> myVec;
	myVec.push_back(pair<string,string>("a","q1"));
	myVec.push_back(pair<string,string>("b","q0"));
	autobot.setFuncaoTransicao("q0",myVec);
	myVec.clear();
	myVec.push_back(pair<string,string>("c","q1"));
	autobot.setFuncaoTransicao("q1",myVec);
	myVec.clear();
	myVec.push_back(pair<string,string>("a","q2"));
	myVec.push_back(pair<string,string>("b","q0"));
	autobot.setFuncaoTransicao("q2",myVec);
	

	autobot.show();
	return 0;	
}

/*	LEITURA DO ARQUIVO
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
*/

/*	DEMONSTRAÇÃO DA ESTRUTURA: FUNÇÕES DE TRANSIÇÃO
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

// map<string, vector<string>> myMap;
// vector<string> aux;
// aux.push_back("outra coisa");
// aux.push_back("mais outra coisa");
// aux.push_back("mais outra coisa ainda");
// myMap.insert(pair<string,vector<string>>("algo",aux));
// cout<<"MYMAP:\n";
// for(auto it:myMap){
// 	cout<<"["<<it.first<<"]: ";
// 	for(int i=0; i<it.second.size();i++){
// 		if(i == (it.second.size()-1)){
// 			cout<<it.second.at(i);
// 		}else{
// 			cout<<it.second.at(i)<<", ";
// 		}
// 	}
// }
// cout<<"\n";

// vector<pair<string, string>> myVec;
// myVec.push_back(pair<string,string>("quero","nao"));
// myVec.push_back(pair<string,string>("quero","nunca"));
// myVec.push_back(pair<string,string>("quero","nananinanunca"));
// cout<<"MYVEC:\n";
// for(int i=0; i<myVec.size(); i++){
// 	if(i == (myVec.size()-1)){
// 		cout<<myVec.at(i).first<<"|"<<myVec.at(i).second;
// 	}else{
// 		cout<<myVec.at(i).first<<"|"<<myVec.at(i).second<<", ";
// 	}
// }
// cout<<"\n";