#pragma once
#include <iostream>
#include <string>

#include "Point.h"

class Classifier;

using std::string;	using std::ostream;


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
