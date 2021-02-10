#include<iostream>
#include<fstream>

using namespace std;

class FileOutput{
	private:
		string m_Path = "../automata/";
		string m_TypeOfFile = ".txt";
	public:
		FileOutput();

		createAutomata(){
			cout<<"Criando um automata.\n\n";
			string temp;
			cout<<"Digite o tipo do automata:\n";
			cout<<"1) AFD;\n";

			switch(opt){
				case 1:
					createAFD("AFD");
					break;
				default:
					cout<<"Opcao invalida.\n\n";
					break; 
			}
		}

		createAFD(string name){}
}typedef FO;