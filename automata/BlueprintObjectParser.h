#pragma once
#include<SFML/Graphics.hpp>
#include<string>
#include"GameObjectBlueprint.h"

using namespace std;
using namespace sf;

class BlueprintObjectParser{
	private:
		string extractStringBetweenTags(string stringToSearch, string startTag, string endTag);
	
	public:
		void parseNextObjectForBlueprint(ifstream& reader, GameObjectBlueprint& bp);
};