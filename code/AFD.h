#include"Automata.h"
#include<iostream>
#include<vector>

using namespace std;

// class Automata;

class AFD : public Automata{
	public:
		AFD(string filename);

		//	PARTES DO AUTOMATA.H
		bool Automata::verificaCadeia(string entrada){
			cout<<"Entrada: "<<entrada<<"\n\n";
			return true;
		}
};