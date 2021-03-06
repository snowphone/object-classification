import re
from functools import reduce
from itertools import chain, dropwhile
from math import hypot, sqrt
from operator import add, sub
from statistics import mean
from sys import argv

from frame import frameInfo
from rectangle import rectangle


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
	#histo(frames)

	with open(basename+"_classified.txt", mode='w+') as file:
		file.writelines((str(frame) for frame in frames))
	print("\a")
	return


def preprocess(lines: list):
	'''텍스트 파일로부터 정보를 받아 frameData 리스트를 반환한다.'''
	frames = []
	delimiter = re.compile(r"\d+")
	frames.append(frameInfo())
	for line in lines:
		if line == '\n' or delimiter.match(line):
			frames.append(frameInfo())
		else:
			frames[-1].append(rectangle(line))
	return [frame for frame in frames if frame]


def tplsub(x: tuple, y: tuple):
	'''튜플간 뺄셈한 결과를 반환한다.'''
	return tuple(map(sub, x, y))


def classify(frames: list, backthrough=3):
	''' 이전 backthrough개의 프레임 속 객체 중 가장 근접한 객체와 현재 객체를 매칭한다.'''

	def distance(x: tuple, y: tuple):
		'''두 이차원 튜플간 유클리드 거리를 계산하여 반환한다.'''
		diff = tplsub(x, y)
		return hypot(*diff)

	#가장 근접한 좌표를 반환
	def find_close_object(currentObj: rectangle, prevFrames, threshold=150):
		'''
		이전 프레임들에 있는 객체들과 비교해, 가장 근접한 객체를 반환한다. 
		단, 가장 근접한 객체와의 거리가 기준치보다 먼 경우, 자기 자신을 반환한다.
		'''
		prevObjs = chain(*prevFrames)
		cand: rectangle = min(
			prevObjs, key=lambda obj: distance(currentObj.center, obj.center))

		if distance(cand.center, currentObj.center) < threshold:
			return cand
		else:
			currentObj.obj = rectangle.usedNum + 1
			return currentObj

	''' 객체 분류 대신 새로운 객체로 인식할 경우 id 이름을 연속해서 사용하기 위함. '''
	rectangle.usedNum = len(frames[:backthrough])

	#첫 프레임은 매칭할 것이 없으므로, 두번째 프레임부터 최대 n개의 프레임을 보고 매칭을 시도한다.
	for idx in range(1, len(frames)):
		currentFrame = frames[idx]
		prevFrames = frames[max(idx - backthrough, 0): idx]
		for currentObj in currentFrame:
			most_similar: rectangle = find_close_object(currentObj, prevFrames)
			currentObj.obj = most_similar.obj
			rectangle.usedNum = max(rectangle.usedNum, currentObj.obj)
	return frames


def histo(frames: list):
	'''디버깅용'''
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
