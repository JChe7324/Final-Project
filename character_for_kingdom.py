import pygame
import math 
import random


class Character(pygame.sprite.Sprite):
	def __init__(self, inital_x, inital_y):
		super().__init__()


		# frames for each animation
		man_walk_frames = 6
		man_attack_frames = 4
		man_hurt_frames = 2
		man_dead_frames = 4
		scale_up = 5 

		# graphics
		man_walk = pygame.image.load('graphics/char/man_walk.png').convert_alpha()
		man_idle = pygame.image.load('graphics/char/man.png').convert_alpha()
		man_attack = pygame.image.load('graphics/char/man_attack.png').convert_alpha()
		man_hurt = pygame.image.load('graphics/char/man_hurt.png').convert_alpha()
		man_dead = pygame.image.load('graphics/char/man_death.png').convert_alpha()

		SHEET_WIDTH, SHEET_HEIGHT = man_walk.get_size()
		frame_width = SHEET_WIDTH // man_walk_frames
		frame_height = SHEET_HEIGHT

		# walk animations
		self.frames = []
		for i in range(man_walk_frames):
			rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
			frame = man_walk.subsurface(rect)
			frame = pygame.transform.scale(frame, (frame_width * scale_up, frame_height * scale_up))
			self.frames.append(frame)

		SHEET_WIDTH2, SHEET_HEIGHT2 = man_attack.get_size()
		frame_width2 = SHEET_WIDTH2 // man_attack_frames
		frame_height2 = SHEET_HEIGHT2

		# attack animations
		self.frames2 = []
		for i in range(man_attack_frames):
			rect2 = pygame.Rect(i * frame_width2, 0, frame_width2, frame_height2)
			frame2 = man_attack.subsurface(rect2)
			frame2 = pygame.transform.scale(frame2, (frame_width2 * scale_up, frame_height2 * scale_up))
			self.frames2.append(frame2)

		SHEET_WIDTH3, SHEET_HEIGHT3 = man_hurt.get_size()
		frame_width3 = SHEET_WIDTH3 // man_hurt_frames
		frame_height3 = SHEET_HEIGHT3

		# Hurt animation
		self.frames3 = []
		for i in range(man_hurt_frames):
			rect3 = pygame.Rect(i * frame_width3, 0, frame_width3, frame_height3)
			frame3 = man_hurt.subsurface(rect3)
			frame3 = pygame.transform.scale(frame3, (frame_width3 * scale_up, frame_height3 * scale_up))
			self.frames3.append(frame3)

		SHEET_WIDTH4, SHEET_HEIGHT4 = man_dead.get_size()
		frame_width4 = SHEET_WIDTH4  // man_dead_frames
		frame_height4 = SHEET_HEIGHT4

		# death animation
		self.frames4 = []
		for i in range(man_dead_frames):
			rect4 = pygame.Rect(i * frame_width4, 0, frame_width4, frame_height4)
			frame4 = man_dead.subsurface(rect4)
			frame4 = pygame.transform.scale(frame4, (frame_width4 * scale_up, frame_height4 * scale_up))
			self.frames4.append(frame4)


		# idle animation
		man_width, man_height = man_idle.get_size()
		self.man_idle = pygame.transform.scale(man_idle, (frame_width * scale_up, frame_height * scale_up))

		#char pos
		self.x_pos = inital_x
		self.y_pos = inital_y

		#aniamtion management
		self.character_state = 'idle'
		self.current_animation_frames = [self.man_idle]
		self.current_frame_index = 0
		self.animation_speed = 100
		self.last_frame_time = pygame.time.get_ticks()

		self.is_attacking = False
		self.is_hurt = False
		self.is_dead = False
		self.movement_speed = 5

		self.facing_right = True
		self.original_walk_frames = self.frames[:]
		self.original_attack_frames = self.frames2[:]
		self.original_hurt_frames = self.frames3[:]
		self.original_dead_frames = self.frames4[:]
		self.original_man_idle = self.man_idle.copy()

		self.attack_damage = 20 
		self.attack_active_frames = [1,2]
		self.has_dealt_damage = False



		self.image = self. current_animation_frames[self.current_frame_index]
		self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))


		self.health = 100

	def update_postions(self, keys):

		if self.is_attacking or self.is_hurt:
			return False

		moving = False
		if keys[pygame.K_a]:
			self.x_pos -= self.movement_speed
			self.facing_right = False
			moving = True
		if keys[pygame.K_d]:
			self.x_pos += self.movement_speed
			self.facing_right = True
			moving = True
		if keys[pygame.K_w]:
			self.y_pos -= self.movement_speed
			moving = True
			if self.y_pos <= 400:
				self.y_pos = 410
		if keys[pygame.K_s]:
			self.y_pos += self.movement_speed
			moving = True
			if self.y_pos >= 600:
				self.y_pos = 590


		self.rect.topleft = (self.x_pos, self.y_pos)

		return moving

	def set_state(self, new_state):

		if self.character_state != new_state:
			self.character_state = new_state
			self.current_frame_index = 0
			self.last_frame_time = pygame.time.get_ticks()

			self.is_attacking = False
			self.is_hurt = False
			self.has_dealt_damage = False


			if self.character_state == 'idle':
				self.current_animation_frames = [self.original_man_idle]

			elif self.character_state == 'walking':
				self.current_animation_frames = self.original_walk_frames

			elif self.character_state == 'attacking':
				self.current_animation_frames = self.original_attack_frames
				self.is_attacking = True
				self.has_dealt_damage =False

			elif self.character_state == 'hurt':
				self.current_animation_frames = self.original_hurt_frames
				self.is_hurt = True

			elif self.character_state == 'dead':
				self.current_animation_frames = self.original_dead_frames
				self.is_dead = True


	def start_attack(self):

		if not self.is_attacking and not self.is_hurt and not self.is_dead:
			self.set_state('attacking')

	def take_damage(self, damage):
		if self.character_state == 'dead':
			return


		self.health -= damage
		if self.health <= 0:
			self.health = 0
			self.set_state('dead')
		else:
			if not self.is_hurt:
				self.set_state('hurt')



	def is_attack_hitting(self):
		if self.is_attacking and self.current_frame_index in self.attack_active_frames and not self.has_dealt_damage:
			return True
		return False


	def notify_damage_dealt(self):
		self.has_dealt_damage = True



	def update(self, keys):

		self.update_postions(keys)
		is_moving = self.update_postions(keys)

		if not self.is_attacking and not self.is_hurt and not self.is_dead:
			if is_moving:
					if self.character_state != 'walking':
						self.set_state('walking')
			else:
					if self.character_state != 'idle':
						self.set_state('idel')


		current_time = pygame.time.get_ticks()

		if not self.current_animation_frames:
			self.image = self.man_idle
			return

		if current_time - self.last_frame_time > self.animation_speed:
			self.current_frame_index += 1
			self.last_frame_time = current_time

			if self.current_frame_index >= len(self.current_animation_frames):

				if self.character_state == 'attacking':
					self.is_attacking = False
					self.current_frame_index = 0

					if keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]:
					   	 self.set_state('walking')

					else:
						self.set_state('idle')

				elif self.character_state == 'hurt':
					self.is_hurt = False
					self.current_frame_index = 0

					if self.health <= 0:
						self.set_state('dead')
					else:
						if keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]:
							self.set_state('walkin')
						else:
							self.set_state('idle')

				elif self.character_state == 'dead':
					self.current_frame_index = len(self.current_animation_frames) - 1
					self.is_dead = True


				else:
					self.current_frame_index %= len(self.current_animation_frames)

		if self.current_animation_frames:

			if self.character_state == 'idle':
				self.image = self.original_man_idle
			elif self.character_state == 'walking':

				if self.current_frame_index < len(self.original_walk_frames):
					self.image = self.original_walk_frames[self.current_frame_index]
				else:
					self.image = self.original_walk_frames[0]

			elif self.character_state == 'dead':
				if self.current_frame_index < len(self.original_dead_frames):
					self.image = self.original_dead_frames[self.current_frame_index]
				else:
					self.image = self.original_dead_frames[0]

			elif self.character_state == 'hurt':
				if self.current_frame_index < len(self.original_hurt_frames):
					self.image = self.original_hurt_frames[self.current_frame_index]
				else:
					self.image = self.original_hurt_frames[0]

			elif self.character_state == 'attacking':
				if self.current_frame_index < len(self.original_attack_frames):
					self.image = self.original_attack_frames[self.current_frame_index]
				else:
					self.image = self.original_attack_frames[0]
			else:
				self.image = self.original_man_idle
			
			


			if not self.facing_right:

				self.image = pygame.transform.flip(self.image, True, False)