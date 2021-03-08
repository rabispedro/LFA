#include<iostream>
#include<cassert>

using namespace std;

void test();

int main(){
	test();

	cout<<"& operator\n";
	cout<<(0x10 & 0x11)<<" ";
	cout<<(0x11 & 0x100)<<" ";
	cout<<(0x100 & 0x1110)<<" ";
	cout<<(0x1110 & 0x1010)<<"\n";


	cout<<"Finished!\n";
	return 0;
}

void test(){
	assert(false == false);
	assert(false != true);
	assert(true == true);
	assert(true != false);

	assert((true && false) == false);

	assert((true || false) == true);

	assert((1 & 0) == 0);
	assert((1 & 1) == 1);

	assert((1 | 0) == 1);
	assert((1 | 1) == 1);
}
