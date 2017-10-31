class Story:
	def __init__(self, num_pages):
		self.num_pages = num_pages
		self.events = self.init_events()
	def init_events(self):
		events = []
		for i in range(self.num_pages):
			event = ''
			if i == 0:
				event = 'birth'
			elif i == self.num_pages - 1:
				event = 'death'
			else:
				event = 'lol'
			events.append(event)
def lol():
	print('lol')