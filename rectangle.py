import re
from statistics import mean


class rectangle(object):
	engine = re.compile(
		r"left=(\d+), right=(\d+), top=(\d+), bottom=(\d+).*obj=(\w+)")
	identifier = 1  # 객체 생성시 각 객체에 고유한 번호를 부여한다.
	usedNum = 1  # 객체 번호를 최대한 낮추기 위한 필드

	def __init__(self, line: str):
		parsedData = rectangle.engine.match(line)

		if not parsedData:
			raise RuntimeError(line)

		self.left = int(parsedData.group(1))
		self.right = int(parsedData.group(2))
		self.top = int(parsedData.group(3))
		self.bottom = int(parsedData.group(4))
		#공 객체가 아닌, 플레이어 객체만 가져옴.
		if parsedData.group(5) == "player":
			self.obj = rectangle.identifier
			rectangle.identifier += 1
		else:
			self.obj = 0  # 공을 판별하기 위함

		self.center = tuple(
                    map(mean, zip(self.topLeftCorner(), self.bottomRightCorner()))
                )
		return

	def __str__(self):
		return "left={}, right={}, top={}, bottom={}, obj_id=0, obj={}\n".format(self.left, self.right, self.top, self.bottom, self.obj)

	def topLeftCorner(self):
		return (self.left, self.top)

	def bottomRightCorner(self):
		return (self.right, self.bottom)
