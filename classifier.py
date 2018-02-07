from sys import argv
from operator import sub, add
from functools import reduce
from math import sqrt, hypot
from statistics import mean
from itertools import dropwhile, chain
import re
'''
TODO: 항상 앞의 n개의 이름을 매칭하므로, 적절한 정확도 이하일 경우 매칭을 포기하도록 개선.
'''


def main():
	name = "output(1).txt"
	with open(name) as file:
		lines = file.readlines()

	#입력된 텍스트 파일 앞 뒤에 있는 공백을 제거한다.
	lines = list(dropwhile(lambda x: x == '\n', lines))
	lines = list(dropwhile(lambda x: x == '\n', reversed(lines)))
	lines = list(reversed(lines))

	frames = preprocess(lines)
	classify(frames)

	#파일 저장
	basename = name[:name.find('.')]
	histo(frames)

	with open(basename+"_classified.txt", mode='w+') as file:
		file.writelines((str(frame) for frame in frames))
	print("\a")

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

class frameData(object):
	'''각 프레임 별 객체를 저장'''
	def __init__(self, objects=None):
		if objects:
			self.objects = objects
		else:
			self.objects = []
		return

	def append(self, data: rectangle):
		if data.obj:
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
	'''텍스트 파일로부터 정보를 받아 frameData 리스트를 반환한다.'''
	frames = []
	delimiter = re.compile(r"\d+")
	frames.append(frameData())
	for line in lines:
		if line == '\n' or delimiter.match(line):
			frames.append(frameData())
		else:
			frames[-1].append(rectangle(line))
	return [frame for frame in frames if frame]


def tplsub(x: tuple, y: tuple):
	'''튜플간 뺄셈한 결과를 반환한다.'''
	return tuple(map(sub, x, y))

def classify(frames: list, backthrough=3):
	''' 이전 n-frame 을 관찰하여 각 객체를 분류한다. '''
	def distance(x: tuple, y: tuple):
		'''두 이차원 튜플간 유클리드 거리를 계산하여 반환한다.'''
		diff = tplsub(x, y)
		return hypot(*diff)

	#가장 근접한 좌표를 반환
	def find_similar(currentObj: rectangle, prevFrames, threshold=150):
		'''
		이전 프레임들에 있는 객체들과 비교해, 가장 근접한 객체를 반환한다. 
		단, 가장 근접한 객체와의 거리가 기준치보다 먼 경우, 자기 자신을 반환한다.
		'''
		cand: rectangle = min(
			chain(*prevFrames), key=lambda obj: distance(currentObj.center, obj.center))

		if distance(cand.center, currentObj.center) < threshold:
			return cand
		else:
			currentObj.obj = rectangle.usedNum + 1
			return currentObj

	rectangle.usedNum = len(frames[:backthrough])

	#첫 프레임은 매칭할 것이 없으므로, 두번째 프레임부터 최대 n개의 프레임을 보고 매칭을 시도한다.
	for idx in range(1, len(frames)):
		currentFrame = frames[idx]
		prevFrames = frames[max(idx - backthrough, 0): idx]
		for currentObj in currentFrame:
			most_similar: rectangle = find_similar(currentObj, prevFrames)
			currentObj.obj = most_similar.obj
			rectangle.usedNum = max(rectangle.usedNum, currentObj.obj)
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
	main()