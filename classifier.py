from sys import argv
from operator import sub 
from functools import reduce
from math import sqrt
import re

class data(object):
	engine = re.compile(r"left=(\d+), right=(\d+), top=(\d+), bottom=(\d+).*obj=(\w+)")
	identifier = 1

	def __init__(self, line : str):
		parsedData = data.engine.match(line)

		if not parsedData:
			raise RuntimeError("포맷에 맞지 않음")
		
		self.left = int(parsedData.group(1))
		self.right = int(parsedData.group(2))
		self.top = int(parsedData.group(3))
		self.bottom = int(parsedData.group(4))
		if parsedData.group(5) == "player":
			self.obj = data.identifier
			data.identifier += 1
		else:
			self.obj = 0	#공을 판별하기 위함
		self.vector = None

		avg = lambda x: (x[0] + x[1]) / 2
		self.center = tuple(map(avg, zip(self.upPosition(), self.downPosition())))
		return

	def __str__(self):
		return "left={}, right={}, top={}, bottom={}, obj_id=0, obj={}".format(self.left, self.right, self.top, self.bottom, self.obj)

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
		if data.obj :
			self.objects.append(data)
		return
	def __str__(self):
		ret = ""
		for obj in self.objects:
			ret += str(obj) + '\n'
		return ret
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

def tplsub(x,y):
	return tuple(map(sub,x,y))

def calculatePositionVector(frame: frameData):
	#왼쪽 아래의 점을 원점으로 삼아 위치벡터 계산
	vectors = [obj.center for obj in frame]
	origin = min(vectors)
	for obj in frame: 
		obj.vector = tplsub(obj.center, origin)
	return

def classify(frames: list):
	def distance(x,y):
		a = tplsub(x,y)
		return sqrt(a[0] ** 2 + a[1] ** 2)

	for frame in frames: 
		calculatePositionVector(frame)

	for idx in range(1, len(frames)):
		prevFrame = frames[idx-1]
		currentFrame = frames[idx]
		for prevObj in prevFrame:
			most_similar = min(currentFrame, key=lambda obj: distance(prevObj.vector, obj.vector))
			most_similar.obj = prevObj.obj
	return frames

def histo(frames: list):
	h = [obj for frame in frames
            for obj in frame]
	M = dict()
	for i in h:
		idx = i.obj
		if idx in M:
			M[idx] += 1
		else:
			M[idx] = 1
	
	for dt in M.items():
		print(dt)
	print(len(M))

if __name__ == "__main__":
	with open("output.txt") as file:
		lines = file.readlines()		
	frames = preprocess(lines)	
	classify(frames)
	print(*frames, sep='\n')
	#histo(frames)