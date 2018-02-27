#pragma once
#include <iostream>
#include <string>
#include <vector>

#include "Object.h"

using std::vector;	using std::ostream;
using std::endl;

class Frame
{
	friend ostream& operator<<(ostream& os, const Frame& frame);
public:
	Frame();
	~Frame();
	Frame& Append(const Object& obj);
	bool IsEmpty() const;
	size_t Size() const;
	vector<Object>& ObjectList();
	const vector<Object>& ObjectList() const;
private:
	vector<Object> mList;
};

ostream& operator<<(ostream& os, const Frame& frame);
