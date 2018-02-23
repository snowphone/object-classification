#include "Frame.h"


Frame::Frame()
{
}


Frame::~Frame()
{
}

Frame & Frame::Append(const Object & obj)
{
	//선수만 취사 선택(현재 공 인식률이 낮음)
	if(obj.GetType() == Object::Type::player)
		mList.push_back(obj);
	return *this;
}

bool Frame::IsEmpty() const
{
	return mList.empty();
}

size_t Frame::Size() const
{
	return mList.size();
}

vector<Object>& Frame::ObjectList() 
{
	return mList;
}

const vector<Object>& Frame::ObjectList() const
{
	return mList;
}

ostream& operator<<(ostream& os, const Frame& frame)
{
	for(const Object& obj : frame.mList)
	{
		os << obj << endl;
	}
	return os;
}
