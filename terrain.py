import os, binascii
import generators

class Terrain:
	def __init__(self, height=800, seed=binascii.b2a_hex(os.urandom(16))):
		self.seed = str(seed)
		self.generator = None
		self.height = height
		self.chunks = {}
		self.loaded = []
		print "Initialised 'Terrain' object, with seed %s, and height %i" % (self.seed, self.height)

	def set_generator(self, generator):
		self.generator = generator

	def load_chunk(self, chunk):
		self.chunks[chunk] = self.generator(chunk, self.height, self.seed)
		self.loaded = list(self.chunks)

	def unload_chunk(self, chunk):
		try: del self.chunks[chunk]
		except KeyError: pass
		self.loaded = list(self.chunks)