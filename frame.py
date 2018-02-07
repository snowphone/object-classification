from rectangle import rectangle


class frameInfo(object):
	'''각 프레임 별 객체를 저장'''

	def __init__(self, objects: rectangle = None):
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
