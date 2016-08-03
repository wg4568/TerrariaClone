import pygame, math, terrain, generators
pygame.M_1 = 323
pygame.M_2 = 324
pygame.M_3 = 325

def convert_coords(x, y):
	offsetx = config.size[0]/2/config.tilesize
	offsety = config.size[1]/2/config.tilesize

	x = (x-player.x+offsetx)*config.tilesize
	y = config.size[1]-(y-player.y+offsety)*config.tilesize
	return [x, y]

def revert_coords(x, y):
	offsetx = config.size[0]/2/config.tilesize
	offsety = config.size[1]/2/config.tilesize

	x = (x/config.tilesize)-(config.size[0]/2/config.tilesize)+player.x
	y = ((config.size[1]-y)/config.tilesize)-(config.size[1]/2/config.tilesize)+player.y
	return [x, y]

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def get_mouse_pos():
	actual = pygame.mouse.get_pos()
	actx = actual[0]
	acty = actual[1]

	return revert_coords(actx + config.mouseoffset[0], acty + config.mouseoffset[1])

def control_check():
	keys = list(pygame.key.get_pressed())
	mouse = pygame.mouse.get_pressed()

	keys.append(mouse[0])
	keys.append(mouse[1])
	keys.append(mouse[2])

	return keys

def extract_chunks(extract_from):
	extracted = {}
	to_extract = required_chunks()
	chunk_low = min(to_extract)
	chunk_high = max(to_extract)
	chunk_range = xrange(chunk_low, chunk_high+1)
	for chunk in chunk_range:
		extracted[chunk] = extract_from[chunk]
	return extracted

def get_corners():
	xoff = config.size[0]/config.tilesize/2
	yoff = config.size[1]/config.tilesize/2
	bl = (player.x - xoff, player.y - yoff)
	br = (player.x + xoff, player.y - yoff)
	tl = (player.x + xoff, player.y - yoff)
	tr = (player.x + xoff, player.y + yoff)
	return bl, br, tl, tr

def current_chunk():
	return int(math.ceil(player.x/10.))

def required_chunks():
	off = config.size[0]/2/config.tilesize
	req = int(math.ceil(off/10.))
	cur = current_chunk()
	bot = cur - req
	top = cur + req + 1
	return xrange(bot, top)

class config:
	size = (500, 500)
	background = (0, 0, 0)
	title = "Test Game"
	rate = 60
	tilesize = 10
	void = "V"
	mouseoffset = (0, -5)
	sky = "K"

class controls:
	up = pygame.K_w
	down = pygame.K_s
	left = pygame.K_a
	right = pygame.K_d
	dig = pygame.M_1
	place = pygame.M_3

	hb_1 = pygame.K_1
	hb_2 = pygame.K_2
	hb_3 = pygame.K_3
	hb_4 = pygame.K_4

class player:
	movespeed = 1
	holding = "S"
	x = 200
	y = 1000

print "Loading textures..."
unscaled_textures = {}
textures = {}
try: unscaled_textures["G"] = pygame.image.load("textures/grass.png")
except pygame.error: print "Missing texture 'G'"; unscaled_textures["G"] = pygame.image.load("textures/missing.png")
try: unscaled_textures["V"] = pygame.image.load("textures/void.png")
except pygame.error: print "Missing texture 'V'"; unscaled_textures["V"] = pygame.image.load("textures/missing.png")
try: unscaled_textures["S"] = pygame.image.load("textures/stone.png")
except pygame.error: print "Missing texture 'S'"; unscaled_textures["S"] = pygame.image.load("textures/missing.png")
try: unscaled_textures["D"] = pygame.image.load("textures/dirt.png")
except pygame.error: print "Missing texture 'D'"; unscaled_textures["D"] = pygame.image.load("textures/missing.png")
try: unscaled_textures["E"] = pygame.image.load("textures/emerald.png")
except pygame.error: print "Missing texture 'E'"; unscaled_textures["E"] = pygame.image.load("textures/missing.png")
try: unscaled_textures["R"] = pygame.image.load("textures/ruby.png")
except pygame.error: print "Missing texture 'R'"; unscaled_textures["R"] = pygame.image.load("textures/missing.png")
try: unscaled_textures["K"] = pygame.image.load("textures/sky.png")
except pygame.error: print "Missing texture 'K'"; unscaled_textures["K"] = pygame.image.load("textures/missing.png")

for texture in unscaled_textures:
	textures[texture] = pygame.transform.scale(unscaled_textures[texture], [config.tilesize]*2)



class World:
	def __init__(self, terrain, *args):
		self.terrain = terrain
		self.objects = args

	def update(self):
		required = required_chunks()
		for chunk in required:
			if not chunk in self.terrain.loaded:
				self.terrain.load_chunk(chunk)

	def draw_terrain(self, screen):
		to_draw = extract_chunks(self.terrain.chunks)
		print to_draw
		merged = merge_dicts(*to_draw.values())

		for tile in merged:
			converted = convert_coords(*tile)
			image = textures[merged[tile]]
			screen.blit(image, converted)
		print converted

	def draw_objects(self, screen):
		for obj in self.objects:
			obj.draw(screen)

	def draw(self, screen):
		screen.fill(config.background)
		self.draw_terrain(screen)
		self.draw_objects(screen)

class Game:
	def __init__(self, world):
		pygame.init()

		self.running = False
		self.frame = 0
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(config.size)
		self.font = pygame.font.Font('freesansbold.ttf', 12)

		self.world = world

		pygame.display.set_caption(config.title)

	def movement(self):
		keys = control_check()
		mouse_pos = get_mouse_pos()

		changex = 0
		changey = 0

		if keys[controls.up]:
			changey += player.movespeed
		if keys[controls.down]:
			changey -= player.movespeed
		if keys[controls.right]:
			changex += player.movespeed
		if keys[controls.left]:
			changex -= player.movespeed

		player.x += changex
		player.y += changey

	def draw(self):
		self.world.draw(self.screen)

		text = self.font.render("(%i, %i)" % (player.x, player.y), True, (100, 100, 100))
		self.screen.blit(text, (config.size[0]-80, 10))

	def start(self):
		self.running = True
		while self.running:
			self.frame += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			self.movement()
			self.world.update()
			self.draw()

			pygame.display.update()
			self.clock.tick(config.rate)

terra = terrain.Terrain()
terra.set_generator(generators.basic_hills)
world = World(terra)
game = Game(world)
game.start()