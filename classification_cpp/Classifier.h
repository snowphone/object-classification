#pragma once
#include <algorithm>
#include <fstream>
#include <string>
#include <vector>
#include <regex>

#include "Frame.h"
#include "Object.h"

using std::string;		using std::vector;
using std::ifstream;	using std::ofstream; 
using std::regex;		using std::regex_search;


class Classifier
{
public:
	Classifier();
	Classifier(const string& path);

	Classifier& Classify(const size_t backthrough = 3);
	Classifier& Read(const string& path);
	Classifier& Write(const string& name);
private:
	const Object& findTheClosestObject(const Object & objToClassify, const vector<Frame>& prevFrames, const size_t threshold = 100ul);
	void reIdentificate();	//ID번호를 앞으로 당긴다.
	string path;
	vector<Frame> mFrameList;
};

