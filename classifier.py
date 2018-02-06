from sys import argv
from operator import sub
from functools import reduce
import re

class data(object):
	engine = re.compile(r"left=(\d+), right=(\d+), top=(\d+), bottom=(\d+).*obj=(\w+)")

	def __init__(self, line: str):
		parsedData = self.engine.match(line)

		if not parsedData:
			raise RuntimeError("포맷에 맞지 않음")
		
		self.left = int(parsedData.group(1))
		self.right = int(parsedData.group(2))
		self.top = int(parsedData.group(3))
		self.bottom = int(parsedData.group(4))
		self.obj = parsedData.group(5)

		avg = lambda x: (x[0] + x[1]) / 2
		self.center = tuple(map(avg, zip(self.upPosition(), self.downPosition())))
		return

	def __str__(self):
		return "left={}, right={}, top={}, bottom={}, obj={}".format(self.left, self.right, self.top, self.bottom, self.obj)

	def upPosition(self):
		return (self.left, self.top)

	def downPosition(self):
		return (self.right, self.bottom)

class frameData(object):
	def __init__(self, objects=None):
		if objects:
			self.objects = objects
		else:
			self.objects = []
		return
	def append(self, data: data):
		if data.obj == "player":
			self.objects.append(data)
		return
	def __str__(self):
		add = lambda x,y: str(x) + str(y) + ' '
		return reduce(add, self.objects)
	def __len__(self):
		return len(self.objects)
	def __iter__(self):
		return (obj for obj in self.objects)
		
def preprocess(lines: list):
	frames = []
	frames.append(frameData())
	for line in lines:
		if line != '\n':
			frames[-1].append(data(line))
		else:
			frames.append(frameData())
	return [frame for frame in frames if len(frame) > 0]

def positionVectorize(frame: frameData):
	def tupleSub(x, y): return tuple(map(sub, x, y))
	#왼쪽 아래의 점을 원점으로 삼아 위치벡터로 변환
	records = [(obj.center, obj) for obj in frame]
	origin = min(records)[0]
	return [(tupleSub(position, origin), obj) for position, obj in records]

def histogram(records: list):
	histo = [0 for _ in range(20)]
	for record in records:
		histo[record] += 1
	for i, dt in enumerate(histo):
		print("{}: {}".format(i,dt))
	return

def classify(frames: list):
	vectorizedData = [positionVectorize(frame) for frame in frames]
	[print(v[0], sep='--------------') for v in vectorizedData]
	


if __name__ == "__main__":
	with open("output.txt") as file:
		lines = file.readlines()		
	frames = preprocess(lines)	
	classify(frames)
