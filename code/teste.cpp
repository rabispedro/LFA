#include<iostream>
#include<vector>
#include<utility>

using namespace std;

void clearScreen();

class Automata{
	private:
		vector<string> m_Estados;

		string m_EstadoInicial;
		vector<string> m_EstadosFinais;

		vector<string> m_Alfabeto;

		vector<pair<string,string>> m_FuncaoTransicao;
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

		void setFuncaoTransicao(vector<pair<string,string>> funcaoTransicao){
			m_FuncaoTransicao.clear();
			for(int i=0; i<funcaoTransicao.size(); i++){
				m_FuncaoTransicao.push_back(pair<string,string>(funcaoTransicao.at(i).first,funcaoTransicao.at(i).second));
			}
		}

		vector<pair<string,string>> getFuncaoTransicao(){
			return m_FuncaoTransicao;
		}


		bool verificaCadeia(string entrada);

		string extractStringBetweenTags(string stringToSearch, string startTag, string endTag);

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

/* INTERPRETAÇÃO (pertence ao alfabeto)
{"a", "b", "c"}
{"ALFA", "BETA", "GAMA"}

"abc" -> ERRADO
"a b c" -> CERTO
"ALFABETAGAMA" -> ERRADO
"ALFA BETA GAMA" -> CERTO
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
	vector<pair<string,string>> funcaoTransicao;
	funcaoTransicao.push_back(pair<string,string>("a","q1"));
	funcaoTransicao.push_back(pair<string,string>("b","q2"));
	funcaoTransicao.push_back(pair<string,string>("b","q2"));
	funcaoTransicao.push_back(pair<string,string>("c","q3"));
	funcaoTransicao.push_back(pair<string,string>("d","q0"));
	funcaoTransicao.push_back(pair<string,string>("e","q1"));
	autobot.setFuncaoTransicao(funcaoTransicao);

	cout<<"FUNCAO TRANSICAO:\n";
	for(int i=0; i<funcaoTransicao.size(); i++){
		cout<<"FuncaoTransicao["<<i<<"]: ["<<funcaoTransicao.at(i).first<<"|"<<funcaoTransicao.at(i).second<<"]\n";
	}

	autobot.show();
	return 0;	
}

void clearScreen(){
	cout<<"";
}