/* take a look at these obj_ids
 * 1175, 1573, 1730, 1776, 1822, 2162, 2911, 3061
 */
#include <algorithm>
#include <cassert>
#include <functional>	//reference_wrapper
#include <iostream>
#ifdef _DEBUG
#include <iostream>
#endif

#include "Classifier.h"

using std::remove_if;	using std::endl;
using std::min_element;	using std::min;
using std::max;			using std::reference_wrapper;
using std::ifstream;	using std::ofstream; 

Classifier::Classifier()
{
}

Classifier::Classifier(const string& path)
{
	Read(path);
}

Classifier& Classifier::Classify(const size_t backthrough, const size_t threshold)
{
	//chaining
	vector<reference_wrapper<Object>> objects;
	for (Frame& frame : mFrameList)
	{
		objects.insert(objects.end(), frame.ObjectList().begin(), frame.ObjectList().end());
	}

	mMaxUsedID = backthrough + 1;

	for (auto frameIter = ++mFrameList.begin(); frameIter != mFrameList.end(); ++frameIter)
	{
		for (Object& objToClassify : frameIter->ObjectList())
		{
			auto beg = (frameIter - mFrameList.begin() < backthrough) ? mFrameList.begin() : frameIter - backthrough;
			const Object& closestObj = findTheClosestObject(objToClassify, beg, frameIter, threshold);
			objToClassify.SetID(closestObj.mID);
			mMaxUsedID = max(objToClassify.mID, closestObj.mID);
			assert("objToClassify's ID and closestObj's ID must be equal" && closestObj.mID == objToClassify.mID);
		}
	}
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
	//remove empty frame objects.
	auto it = remove_if(mFrameList.begin(), mFrameList.end(), [](Frame& i) { return i.IsEmpty(); });
	mFrameList.erase(it, mFrameList.end());
	return *this;
}

Classifier& Classifier::Write(const string& name)
{
	ofstream os(name);
	for (const Frame& frame : mFrameList)
	{
		os << frame << endl;
	}
	return *this;
}

const Object& Classifier::findTheClosestObject(
	Object& objToClassify, const_iterator pFrameBeg, const_iterator pFrameEnd, const size_t threshold)
{
	vector<reference_wrapper<const Object>> objects;
	for (auto cIt = pFrameBeg; cIt != pFrameEnd; ++cIt)
	{
		for (const Object& obj : cIt->ObjectList())
		{
			objects.push_back(obj);
		}
	}

	const Object& nearest = *min_element(objects.begin(), objects.end(), [&objToClassify](const Object& l, const Object& r) {
		return Distance(l, objToClassify) < Distance(r, objToClassify);
	});

	if (Distance(nearest, objToClassify) < threshold)
	{
		return nearest;
	}
	else
	{
#ifdef _DEBUG
		std::cout << "------------------" << std::endl
			<< "nearset: " << nearest << std::endl
			<< "object: " << objToClassify << std::endl
			<< "distance: " << Distance(nearest, objToClassify) << std::endl;
#endif
		//reidentificate
		objToClassify.SetID(mMaxUsedID + 1);
		return objToClassify;
	}
}

