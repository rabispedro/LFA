#include<iostream>
#include<vector>

using namespace std;

class Automata{
	private:
		vector<string> m_Estados;

		string m_EstadoInicial;
		vector<string> m_EstadosFinais;

		vector<string> m_Alfabeto;

		vector<vector<string>> m_FuncaoTransicao;

	public:
		vector<string> getEstados();

		string getEstadoInicial();
		vector<string> getEstadosFinais();

		vector<string> getAlfabeto();

		virtual bool verificaCadeia(string entrada) = 0;

		string extractStringBetweenTags(string stringToSearch, string startTag, string endTag);
};

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