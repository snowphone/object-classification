#include "Classifier.h"

int main(int argc, char* argv[]) {
	string path = "../output.txt";
	Classifier classifier;
	classifier.Read(path);
	classifier.Classify();
	classifier.Write("../result.txt");
};