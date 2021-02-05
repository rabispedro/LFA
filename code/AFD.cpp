#include<iostream>
#include<vector>
#include<map>
#include<utility>
#include<fstream>
#include<string>
#include<limits>

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

vector<string> vectorization(string str);
string addSpace(string str);

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
			bool flag;

			//	Verificar se a entrada pertence ao alfabeto
			for(int i=0; i<entrada.size(); i++){
				flag = false;
				for(int j=0; j<alfabeto.size(); j++){
					if(entrada.at(i) == alfabeto.at(j)){
						flag = true;
					}
				}
				if(!flag){
					cout<<"Erro: entrada nao percente ao Alfabeto do Automato.\n\n";
					return false;
				}
				flag = false;
			}

			string estadoAtual = getEstadoInicial();
			map<string,vector<pair<string,string>>> funcaoTransicao = getFuncaoTransicao();
			
			for(int i=0; i<entrada.size(); i++){
				for(auto it: funcaoTransicao){
					if(estadoAtual == it.first){
						cout<<"["<<estadoAtual<<"]---\"";
						for(int j=0; j<it.second.size(); j++){
							if(entrada.at(i) == it.second.at(j).first){
								cout<<entrada.at(i)<<"\"--->";
								estadoAtual = it.second.at(j).second;
								cout<<"["<<estadoAtual<<"]\n";
								break;
							}
						}
						break;
					}
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

			cout<<"Erro: o ultimo estado atingido nao corresponde a nenhum dos estados finais.\n\n";
			return false;
		}

		string extractStringBetweenTags(string stringToSearch, string startTag, string endTag){
			int start = startTag.size();
			int count = (stringToSearch.size() - (startTag.size() + endTag.size()));

			return stringToSearch.substr(start, count);
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
	// string path = "../automata/";
	// string file;
	// cout<<"Digite o nome do arquivo do automato: ";
	// cin>>file;
	// path += file;
	// path += ".txt";
	// AFD autobot(path);

	AFD autobot("../automata/AFD.txt");
	autobot.show();

	string entrada;
	vector<string> myVec;

	//	Cleaning cin
	// cin.clear();
	// cin.ignore(numeric_limits<streamsize>::max(), '\n');
	// fflush(stdin);

	while(true){
		cout<<"Digite uma entrada (separe os simbolos por espacos ou \"sair\"): ";
		getline(cin, entrada);

		if(entrada == "sair"){
			break;
		}

		myVec = vectorization(entrada);
		
		if(autobot.verificaCadeia(myVec)){
			cout<<"Cadeia Aceita!\n\n";
		}else{
			cout<<"Cadeia Rejeitada!\n\n";
		}

		entrada.clear();
		myVec.clear();
	}

	cout<<"Saindo...\n\n";
	return 0;	
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

string addSpace(string str){
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
