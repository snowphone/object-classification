from sys import argv
from operator import sub, add
from functools import reduce
from math import sqrt
from statistics import mean
from itertools import dropwhile, chain
import re
'''
TODO: 항상 앞의 n개의 이름을 매칭하므로, 적절한 정확도 이하일 경우 매칭을 포기하도록 개선.
'''

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

		self.center = tuple(map(mean, zip(self.upPosition(), self.downPosition())))
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
	def __bool__(self):
		return bool(self.objects)
	def __iter__(self):
		return (obj for obj in self.objects)
		
def preprocess(lines: list):
	frames = []
	delimiter = re.compile(r"\d+")
	frames.append(frameData())
	for line in lines:
		if line == '\n' or delimiter.match(line):
			frames.append(frameData())
		else:
			frames[-1].append(data(line))
	return [frame for frame in frames if frame]

def tplsub(x,y):
	return tuple(map(sub,x,y))

def classify(frames: list):
	#유클리드 거리 계산
	def distance(x,y):
		a = tplsub(x,y)
		return sqrt(a[0] ** 2 + a[1] ** 2)

	#가장 근접한 좌표를 반환
	def find_similar(currentObj: data, prevFrames):
		return min(chain(*prevFrames), key=lambda obj: distance(currentObj.center, obj.center))

	backthrough = 1

	data.usedNum = len(frames[:backthrough])
	
	for idx in range(1, len(frames)):
		currentFrame = frames[idx]
		prevFrames = frames[idx - backthrough: idx]
		for currentObj in currentFrame:
			most_similar: data = find_similar(currentObj, prevFrames)
			currentObj.obj = most_similar.obj
			data.usedNum = max(data.usedNum, currentObj.obj)
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
		
	lines = list(dropwhile(lambda x: x == '\n', lines))
	lines = list(dropwhile(lambda x: x == '\n', reversed(lines)))
	lines = list(reversed(lines))

	
	frames = preprocess(lines)	
	classify(frames)

	basename = name[:name.find('.')]
	histo(frames)

	with open(basename+"_classified.txt", mode='w+') as file:
		file.writelines((str(frame) for frame in frames))
	print("\a")
