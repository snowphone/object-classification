#include "Classifier.h"
#include <iostream>


Classifier::Classifier()
{
}

Classifier::Classifier(const string& path)
{
	Read(path);
}

Classifier& Classifier::Classify(const size_t backthrough)
{
	for (auto it = ++mFrameList.begin(); it != mFrameList.end(); ++it)
	{
		if (it->IsEmpty())
			continue;
		for (Object& objToClassify : it->ObjectList())
		{
			auto beg = (it - mFrameList.begin() < backthrough) ? mFrameList.begin() : it - backthrough;
			const Object& closestObj = findTheClosestObject(objToClassify, vector<Frame>(beg, it));
			objToClassify.SetID(closestObj.mID);
			//std::cout << objToClassify << std::endl;
		}
	}
	reIdentificate();
	return *this;
}

Classifier& Classifier::Read(const string& path)
{
	mFrameList.clear();


	ifstream is(path);
	string info;
	while (getline(is, info))
	{
		Object obj(info);
		if (obj.GetType() == Object::Type::header)
		{
			mFrameList.push_back(Frame());
		}
		else
		{
			mFrameList.back().Append(obj);
		}
	}
	auto it = std::remove_if(mFrameList.begin(), mFrameList.end(), [](Frame& i) {return i.IsEmpty(); });
	mFrameList.erase(it, mFrameList.end());
	return *this;
}

Classifier& Classifier::Write(const string& name)
{
	ofstream os(name);
	for (const Frame& frame : mFrameList)
	{
		os << frame << std::endl;
	}
	return *this;
}

const Object& Classifier::findTheClosestObject(const Object& objToClassify, const vector<Frame>& prevFrames, const size_t threshold)
{
	vector<std::reference_wrapper<const Object>> objects;
	for (const Frame& frame : prevFrames)
	{
		for (const Object& obj : frame.ObjectList())
		{
			objects.push_back(obj);
		}
	}
	const Object& cand = *std::min_element(objects.begin(), objects.end(), [&objToClassify](const Object& l, const Object& r) {
		return Distance(l, objToClassify) < Distance(r, objToClassify);
	});
	return Distance(cand, objToClassify) < threshold ? cand : objToClassify;
}

//ID 번호를 1번부터 차례대로 사용하도록 정리한다.
void Classifier::reIdentificate()
{
	vector<std::reference_wrapper<Object>> objects;
	for (Frame& frame : mFrameList)
	{
		objects.insert(objects.end(), frame.ObjectList().begin(), frame.ObjectList().end());
	}

	for (auto it = ++objects.begin(); it != objects.end(); ++it)
	{
		it->get().SetID(std::min(it->get().mID, it[-1].get().mID + 1));
	}
}

