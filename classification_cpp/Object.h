#pragma once
#include <iostream>
#include <string>
#include <regex>

#include "Point.h"

using std::string;
using std::smatch;
using std::regex;
using std::regex_search;
using std::ostream;

class Classifier;

class Object
{
	friend ostream& operator<<(ostream& os, const Object& obj);
	friend class Classifier;
public:
	enum class Type : char { ball, player, header };

	Object();
	explicit Object(const string& info);
	~Object();
	const Point& Center() const;
	Type GetType() const;

private:
	static int identifier;
	void SetID(const int newID);

	Point mLeftTop;
	Point mRightBottom;
	Point mCenter;
	Type mType;
	int mID;
};

ostream& operator<<(ostream& os, const Object& obj);
double Distance(const Object& lhs, const Object& rhs);
