#include"Automata.h"
#include<iostream>
#include<vector>
#include<fstream>

using namespace std;

vector<string> Automata::getEstados(){
	return m_Estados;
}

string Automata::getEstadoInicial(){
	return m_EstadoInicial;
}

vector<string> Automata::getEstadosFinais(){
	return m_EstadosFinais;
}

vector<string> Automata::getAlfabeto(){
	return m_Alfabeto;
}

string Automata::extractStringBetweenTags(string stringToSearch, string startTag, string endTag){
	int start = startTag.size();
	int count = (stringToSearch.size() - (startTag.size() + endTag.size()));

	string temp = stringToSearch.substr(start, count);
	return temp;
}