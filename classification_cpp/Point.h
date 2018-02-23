#pragma once
#include <algorithm>
#include <cmath>

using Point = std::pair<int, int>;

Point operator+(const Point& lhs, const Point& rhs);
Point operator-(const Point& lhs, const Point& rhs);
Point operator/(const Point& point, const int divisor);
double Distance(const Point& lhs, const Point& rhs);
