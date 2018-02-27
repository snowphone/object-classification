#pragma once
#include <algorithm>
#include <fstream>
#include <string>
#include <vector>

#include "Frame.h"

class Object;

using std::string;		using std::vector;


class Classifier
{
public:
	using iterator = vector<Frame>::iterator;
	using const_iterator = vector<Frame>::const_iterator;
	Classifier();
	Classifier(const string& path);

	Classifier& Classify(const size_t backthrough = 3, const size_t threshold = 150ull);
	Classifier& Read(const string& path);
	Classifier& Write(const string& name);
private:
	const Object& findTheClosestObject(Object & objToClassify, const_iterator pFrameBeg, const_iterator pFrameEnd, const size_t threshold);
	string path;
	vector<Frame> mFrameList;
	int mMaxUsedID = 1;
};

