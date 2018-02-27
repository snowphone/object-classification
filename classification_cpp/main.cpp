#include <cassert>
#include <iostream>
#include <string>
#include "Classifier.h"

using namespace std;

int main(int argc, char* argv[]) {
	if (!(argc > 1))
	{
		cout << "You must pass the file as an argument!" << endl;
		return 1;
	}
	string path = argv[1];
	Classifier classifier;
	classifier.Read(path);
	classifier.Classify();
	string output = path.substr(0, path.rfind(".")) + "_cppclassified.txt";
	classifier.Write(output);
};