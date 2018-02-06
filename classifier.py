from sys import argv
from operator import sub, add
from functools import reduce
from math import sqrt
from statistics import mean
import time
import re

class data(object):
	engine = re.compile(r"left=(\d+), right=(\d+), top=(\d+), bottom=(\d+).*obj=(\w+)")
	identifier = 1
	usedNum = 1

	def __init__(self, line : str):
		parsedData = data.engine.match(line)

		if not parsedData:
			raise RuntimeError(line)
		
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
		return "left={}, right={}, top={}, bottom={}, obj_id=0, obj={}\n".format(self.left, self.right, self.top, self.bottom, self.obj)

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
		return "".join((str(obj) for obj in self.objects)) + '\n'
	def __len__(self):
		return len(self.objects)
	def __iter__(self):
		return (obj for obj in self.objects)
		
def preprocess(lines: list):
	frames = []
	delimiter = re.compile(r"\b\d+\b")
	frames.append(frameData())
	for line in lines:
		if delimiter.match(line):
			frames.append(frameData())
		else:
			frames[-1].append(data(line))
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
			prevObj.obj = min(data.usedNum + 1, prevObj.obj)
			most_similar = min(currentFrame, key=lambda obj: distance(prevObj.vector, obj.vector))
			most_similar.obj = prevObj.obj
			data.usedNum = max(data.usedNum, prevObj.obj)
	return frames

def histo(frames: list):
	'''for debuging'''
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
	name = "output(1).txt"
	with open(name) as file:
		lines = file.readlines()		
	frames = preprocess(lines)	
	classify(frames)

	basename = name[:name.find('.')]
	histo(frames)
	with open(basename+"_classified.txt", mode='w+') as file:
		file.writelines((str(frame) for frame in frames))
	#print(*frames, sep='\n')
	#histo(frames)
