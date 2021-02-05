#include<iostream>
#include<vector>
#include<map>
#include<utility>
#include<fstream>

using namespace std;

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


class Automata{
	private:
		string m_Descricao;

		vector<string> m_Estados;

		string m_EstadoInicial;
		vector<string> m_EstadosFinais;

		vector<string> m_Alfabeto;

		map<string,vector<pair<string,string>>> m_FuncaoTransicao;
	public:
		Automata(string filename){
			cout<<"\tFile: "<<filename<<"\n\n";
			ifstream reader(filename);
			string lineFromFile;
			string temp;
			int count=1;
			vector<string> vecStr;
			vector<pair<string,string>> vecPair;
			string estadoAnterior;

			while(getline(reader,lineFromFile)){
				cout<<count++<<"|  "<<lineFromFile<<"\n";
				if(lineFromFile.find("[DESCRICAO]") != string::npos){
					//	Descricao
					temp = extractStringBetweenTags(lineFromFile, "[DESCRICAO]", "[-DESCRICAO]");
					setDescricao(temp);
					temp.clear();
				}else if(lineFromFile.find("[ESTADOS]") != string::npos){
					//	Estados: PRECISA ARRUMAR
					temp = extractStringBetweenTags(lineFromFile, "[ESTADOS]", "[-ESTADOS]");
					setEstados(vectorization(temp));
					temp.clear();
				}else if(lineFromFile.find("[ALFABETO]") != string::npos){
					//	Alfabeto
					temp = extractStringBetweenTags(lineFromFile, "[ALFABETO]", "[-ALFABETO]");
					setAlfabeto(vectorization(temp));
					temp.clear();
				}else if(lineFromFile.find("[FUNCAO TRANSICAO]") != string::npos){
					//	Função Transição

					//	Primeira linha da Função Transição
					getline(reader,lineFromFile);
					while(!(lineFromFile.find("[-FUNCAO TRANSICAO]") != string::npos)){
						vecStr = vectorization(lineFromFile);

							// Primeiro até penúltimo Estado Inicial diferente
						if((estadoAnterior.empty()) || (estadoAnterior == vecStr.at(0))){
							estadoAnterior = vecStr.at(0);
							vecPair.push_back(pair<string, string>(vecStr.at(1), vecStr.at(2)));
						}else{
							setFuncaoTransicao(estadoAnterior, vecPair);
							estadoAnterior.clear();
							vecPair.clear();
							
							//	Adiciona o conteudo do novo estado
							estadoAnterior = vecStr.at(0);
							vecPair.push_back(pair<string, string>(vecStr.at(1), vecStr.at(2)));
						}

						//	Proxima linha da Função Transição
						getline(reader,lineFromFile);
						
						//	Último Estado Atual
						if(lineFromFile.find("[-FUNCAO TRANSICAO]") != string::npos){
							setFuncaoTransicao(estadoAnterior, vecPair);
							estadoAnterior.clear();
							vecPair.clear();
						}
					}

				}else if(lineFromFile.find("[ESTADO INICIAL]") != string::npos){
					//	Estado Inicial
					temp = extractStringBetweenTags(lineFromFile, "[ESTADO INICIAL]", "[-ESTADO INICIAL]");
					setEstadoInicial(temp);
					temp.clear();
				}else if(lineFromFile.find("[ESTADOS FINAIS]") != string::npos){
					//	Estados Finais
					temp = extractStringBetweenTags(lineFromFile, "[ESTADOS FINAIS]", "[-ESTADOS FINAIS]");
					setEstadosFinais(vectorization(temp));
					temp.clear();
				}
			}
			cout<<"\n";
		}

		void setDescricao(string descricao){
			m_Descricao = descricao;
		}

		string getDescricao(){
			return m_Descricao;
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

		void resetFuncaoTransicao(){
			m_FuncaoTransicao.clear();
		}

		bool verificaCadeia(vector<string> entrada){
			vector<string> alfabeto = getAlfabeto();
			bool flag = true;

			//	Verificar se a entrada pertence ao alfabeto
			for(int i=0; i<entrada.size(); i++){
				for(int j=0; j<alfabeto.size(); j++){
					if(entrada.at(i) == alfabeto.at(j)){
						flag = true;
					}
				}
				if(!flag){
					return false;
				}
				flag = false;
			}
			cout<<"Entrada pertence ao alfabeto!\n";

			string estadoAtual = getEstadoInicial();
			map<string,vector<pair<string,string>>> funcaoTransicao = getFuncaoTransicao();
			/*
			cout<<"Funcao Transicao:\n";
			for(auto it : funcaoTransicao){
				cout<<"\t["<<it.first<<"]\n";
				for(int i=0; i<it.second.size();i++){
					cout<<"\t  |---"<<it.second.at(i).first<<"--->["<<it.second.at(i).second<<"]\n";
				}
			}
			cout<<"\n";
			*/
			
			string estadoAvant;

			/*	COLINHA RAPIDA
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

			for(int i=0; i<entrada.size(); i++){
				cout<<"estadoAtual: "<<estadoAtual<<"\n";
				cout<<"simboloAtual: "<<entrada.at(i)<<"\n";
				cout<<"\n";
				for(auto it: funcaoTransicao){
					if(estadoAtual == it.first){
						cout<<"Estado Atual: "<<estadoAtual<<"\n";
						for(int j=0; j<it.second.size(); j++){
							// cout<<"Simbolo Atual: "<<it.second.at(j).first<<"\n";
							if(entrada.at(i) == it.second.at(j).first){
								cout<<"Simbolo Encontrado: "<<entrada.at(i)<<"\n";
								estadoAtual = it.second.at(j).second;
								break;
							}
						}
						break;
					}
					// cout<<"Estado Atual: "<<it.first<<"\n";
					// cout<<"Simbolo Atual: "<<it.second.at(0).first<<"\n";
					// cout<<"Estado Avancado: "<<it.second.at(0).second<<"\n";
					// cout<<"\n\n";
				}
				
			}

			cout<<"ESTADO FINAL: "<<estadoAtual<<"\n";

			//	Verificação do Último Estado da entrada com os Estados Finais do Automato
			vector<string> estadosFinais = getEstadosFinais();
			for(int i=0; i<estadosFinais.size(); i++){
				if(estadoAtual == estadosFinais.at(i)){
					return true;
				}
			}

			return false;
		}

		string extractStringBetweenTags(string stringToSearch, string startTag, string endTag){
			int start = startTag.size();
			int count = (stringToSearch.size() - (startTag.size() + endTag.size()));

			return stringToSearch.substr(start, count);
		}

		vector<string> vectorization(string str){
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

		void show(){
			//	Descrição
			cout<<"Descricao: "<<m_Descricao<<"\n";

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
			cout<<"\n\n";
		}
}typedef AFD;

int main(){
	AFD autobot("AFD.txt");/*

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
	
	//	Testando uso de FLAGS
	string tag = "[TAG]texto inserido entre tags[-TAG]";
	cout<<"String: "<<tag<<"\n";
	cout<<"Processado: "<<autobot.extractStringBetweenTags(tag,"[TAG]","[-TAG]")<<"\n";
	*/

	autobot.show();

	vector<string> myVec;
	myVec.push_back("0");
	myVec.push_back("1");
	myVec.push_back("0");
	myVec.push_back("0");

	cout<<autobot.verificaCadeia(myVec)<<"\n";
	return 0;	
}

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