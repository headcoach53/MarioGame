import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, model, x, y, w, h):
		self.model = model
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	def iam(self):
		pass

	def isBrick(self):
		return False

	def isMario(self):
		return False

	def isCoin(self):
		return False

	def isCoinblock(self):
		return False

	def update(self):
		pass

	def draw(self):
		pass

	def is_inside(self, pos):
		if pos[0] < self.x:
			return False
		if pos[0] > self.x + self.w:
			return False
		if pos[1] < self.y:
			return False
		if pos[1] > self.y + self.h:
			return False
		return True
		

class Mario(Sprite):
	def __init__(self, model, x, y, w, h):
		self.model = model
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.mario_image0 = pygame.image.load("mario1.png")
		self.mario_image1 = pygame.image.load("mario2.png")
		self.mario_image2 = pygame.image.load("mario3.png")
		self.mario_image3 = pygame.image.load("mario4.png")
		self.mario_image4 = pygame.image.load("mario5.png")
		
		self.mario_image_list = []
		self.mario_image_list.append(self.mario_image0)
		self.mario_image_list.append(self.mario_image1)
		self.mario_image_list.append(self.mario_image2)
		self.mario_image_list.append(self.mario_image3)
		self.mario_image_list.append(self.mario_image4)
		
		self.framecount = 0
		self.vert_velo = 0
		self.dest_x = 200;
		self.dest_y = 200;
		self.jump_since_ground = 0
		
	def iam(self):
		return 1

	def isMario(self):
		return True
	
	def remember_prev_pos(self):
		self.prev_x = self.x
		self.prev_y = self.y

	def update(self):
		self.framecount += 1
		if self.framecount > 4:
			self.framecount = 0
		self.vert_velo += 5.2
		self.y += self.vert_velo
		if self.jump_since_ground != 0:
			self.jump_since_ground += 1
		if self.y > 305:
			self.y = 305
			self.jump_since_ground = 0
		
	def draw(self):
		if self.prev_x != self.x:
			v.screen.blit(self.mario_image_list[self.framecount], (self.x-self.model.scrollpos, self.y))
		else:
			v.screen.blit(self.mario_image_list[2],(self.x-self.model.scrollpos, self.y))

class Brick(Sprite):
	def __init__(self,model, x, y, w, h):
		self.model = model
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.Brick_image = pygame.image.load("brick.jpg")

	def iam(self):
		return 2

	def isBrick(self):
		return False

	def draw(self):
		v.screen.blit(self.Brick_image, (self.x-self.model.scrollpos, self.y))

class CoinBlock(Sprite):
	def __init__(self, model, x, y, w, h):
		self.model = model
		self.x = x
		self.y = y
		self.w = 89
		self.h = 83
		self.coins = 5
		self.CoinBlock_image0 = pygame.image.load("block2.png")
		self.CoinBlock_image1 = pygame.image.load("block1.png")

	def iam(self):
		return 3
	def popoutacoin(self):
		self.coins -= 1

	def isCoinblock(self):
		return True

	def draw(self):
			if(self.coins != 0):
				v.screen.blit(self.CoinBlock_image1, (self.x-self.model.scrollpos, self.y))
			else:
				v.screen.blit(self.CoinBlock_image0, (self.x-self.model.scrollpos, self.y))


class Coin(Sprite):
	def __init__(self,model, x, y, w, h):
		self.model = model
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.Coin_image = pygame.image.load("coin.png")
		self.hori_velo = 10
		self.vert_velo = -15
		self.get_rid_of_me = False

	def iam(self):
		return 4
	def isCoin(self):
		return False

	def update(self):
		self.hori_velo -= 1
		if self.hori_velo < 0:
			self.hori_velo = 0;
		self.x += self.hori_velo

		self.vert_velo += 4.5
		self.y += self.vert_velo


	def draw(self):
		v.screen.blit(self.Coin_image, (self.x-self.model.scrollpos, self.y))
				
	
class Model():
		def __init__(self):
			self.mario = Mario(self,200, 200, 60, 95)
			self.brick1 = Brick(self,500, 200, 50, 50)
			self.brick2 = Brick(self,110, 150, 50, 50)
			self.coinblock = CoinBlock(self,348, 93, 89, 83)
			self.scrollpos = 0

			self.sprites = []
			self.sprites.append(self.mario)
			self.sprites.append(self.brick1)
			self.sprites.append(self.brick2)
			self.sprites.append(self.coinblock)

		def add_Brick(self, pos):
			for i in self.sprites:
				if i.is_inside(pos):
					self.sprites.remove(i)
					return
			self.Brick = Brick(self,pos[0], pos[1], 55, 400)
			self.sprites.append(self.Brick)
		def add_CoinBlock(self, pos):
			for i in self.sprites:
				if i.is_inside(pos):
					self.sprites.remove(i)
					return
			self.CoinBlock = CoinBlock(self,pos[0], pos[1], 55, 400)
			self.sprites.append(self.CoinBlock)

		def add_Coin(self):
			self.Coin = Coin(self, self.mario.x, self.mario.y, 47, 47)
			self.sprites.append(self.Coin)			

		def update(self):
				for i in self.sprites:
					i.update()
					if i.iam() == 1:
							self.scrollpos= self.mario.x
					if i.iam() == 2:# I am a Brick
						if self.does_intersect(self.mario, i):
								self.get_out_of_Brick(i)
								   
					if i.iam() == 3:# i am a CoinBlock
						if self.does_intersect(self.mario,i):
							self.get_out_of_CoinBrick(i)
					if i.iam() == 4:
						if i.y >=1000:
							i.y=1000
							i.x=-3000
								#self.sprites.remove(self.Coin)
							
		def does_intersect(self, a, b):
			if a.x + a.w < b.x:
				return False
			if a.x > b.x + b.w:
				return False
			if a.y > b.y + b.h:
				return False
			if a.y + a.h < b.y:
				return False
			return True

		def get_out_of_Brick(self, s):
				if self.mario.x + self.mario.w >= s.x and self.mario.prev_x + self.mario.w <= s.x:
					self.mario.x = s.x - self.mario.w - 1
				
				elif self.mario.x <= s.x + s.w and self.mario.prev_x >= s.x + s.w:
					self.mario.x = s.x + s.w + 1
				elif self.mario.y + self.mario.h >= s.y and self.mario.prev_y + self.mario.h <= s.y:
					self.mario.y = s.y - self.mario.h - 1
					self.mario.jump_since_ground = 0
				elif self.mario.y <= s.y + s.h and self.mario.prev_y >= s.y + s.h:
					self.mario.y = s.y + s.h + 1
	
		def get_out_of_CoinBrick(self, s):
				if self.mario.x + self.mario.w >= s.x and self.mario.prev_x + self.mario.w <= s.x:
					self.mario.x = s.x - self.mario.w - 1
				elif self.mario.x <= s.x + s.w and self.mario.prev_x >= s.x + s.w:
					self.mario.x = s.x + s.w + 1
				elif self.mario.y + self.mario.h >= s.y and self.mario.prev_y + self.mario.h <= s.y:
					self.mario.y = s.y - self.mario.h - 1
					self.mario.jump_since_ground = 0
				elif self.mario.y <= s.y + s.h and self.mario.prev_y >= s.y + s.h:
					self.mario.y = s.y + s.h + 1
					if(self.coinblock.coins is not 0):
						self.coinblock.popoutacoin()
						self.add_Coin()
						sleep(.01)
						self.mario.vert_velo += 50
									
		
class View():
		def __init__(self, model):
				screen_size = (800,600)
				self.screen = pygame.display.set_mode(screen_size, 32)
				self.model = model

		def update(self):    
				self.screen.fill([0,200,100])
				for i in self.model.sprites:
					i.draw()                    
				pygame.display.flip()

class Controller():
		def __init__(self, model):
				self.model = model
				self.keep_going = True

		def update(self):
				for event in pygame.event.get():
						if event.type == QUIT:
								self.keep_going = False
						elif event.type == KEYDOWN:
								if event.key == K_ESCAPE:
										self.keep_going = False
						elif event.type == pygame.MOUSEBUTTONUP:
							if event.button == 1:
								self.model.add_Brick(pygame.mouse.get_pos())
							elif event.button == 3:
								self.model.add_CoinBlock(pygame.mouse.get_pos())
				keys = pygame.key.get_pressed()
				if keys[K_LEFT]:
						self.model.mario.x -= 10
				if keys[K_RIGHT]:
						self.model.mario.x += 10
				if keys[K_DOWN]:
						self.model.mario.y += 1
				if self.model.mario.jump_since_ground < 5:
					if keys[K_SPACE]:
						self.model.mario.vert_velo = -37
						self.model.mario.jump_since_ground += 1
				

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
		m.mario.remember_prev_pos()
		c.update()
		m.update()
		v.update()
		sleep(0.04)
print("Goodbye")
