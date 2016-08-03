from base64 import b64encode, b64decode
import pickle
import os
import zlib

storage_file = "worlds/"
extension = ".world"
compression = True

def get_size(world):
	xmax = 0
	ymax = 0
	for item in world:
		if item[0] > xmax: xmax = item[0]
		if item[1] > ymax: ymax = item[1]
	return xmax+1, ymax+1

def save(obj, name):
	global storage_file, extension
	print "-> Pickling world..."
	data = pickle.dumps(obj)
	print "-> Compressing..."
	data = zlib.compress(data)
	print "-> Converting to base64..."
	data = b64encode(data)
	print "-> Writing to file..."
	open(storage_file + name + extension, "w").write(data)
	print "-> World successfully saved"

def load(name):
	global storage_file, extension
	print "-> Reading from file..."
	data = open(storage_file + name + extension, "r").read()
	print "-> Converting from base64..."
	data = b64decode(data)
	print "-> Decompressing..."
	data = zlib.decompress(data)
	print "-> Converting from pickle..."
	data = pickle.loads(data)
	print "-> World successfully loaded"
	return data

def remove(name):
	global storage_file, extension
	os.remove(storage_file + name + extension)