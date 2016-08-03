#==========================================IMPORTS==================================#
from random import randint as rand, seed as set_seed
from noise import pnoise1, pnoise2
from hashlib import md5
from math import sqrt

#==========================================HELPERS==================================#
def noise1D(val, seed):
	seed = parse_seed(seed)
	return pnoise1((val/100.) + seed)

def noise2D(val1, val2, seed):
	seed = parse_seed(seed)
	return pnoise2((val1/100.) + seed, (val2/100.) + seed)

def translate(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)
	return rightMin + (valueScaled * rightSpan)

def parse_seed(seed):
	h = md5(str(seed)).hexdigest()
	s = translate(int(h, 16), 0, 10**38, 0, 100)
	return s

def get_chunk(x, seed, generator):
	return generator(x, seed)

#======================================GENERATORS===================================#

def basic_hills(x, height, seed):
	set_seed(seed)
	cs = x * 10
	xr = xrange(cs, cs+10)
	chunk = {}
	for x in xr:
		for y in xrange(height):
			top = noise1D(x, seed)
			if y == top:
				chunk[x, y] = "G"
			elif y > top:
				chunk[x, y] = "K"
			elif top-y < rand(3, 7):
				chunk[x, y] = "D"
			else:
				chunk[x, y] = "S"
	return chunk