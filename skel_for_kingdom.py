import pygame
import os
import math
import random



class Enemy(pygame.sprite.Sprite):
	def __init__(self, inital_x, inital_y):
		super().__init__()

		#variables
		skel_walk_frames = 7
		skel_attack_frames = 5
		skel_attack_frames2 = 6
		skel_attack_frames3 = 4
		skel_idle_frames = 7
		skel_dead_frames = 4
		skel_hurt_frames = 2
		scale_up = 3

		skel_walk = pygame.image.load('graphics/char/Walk.png').convert_alpha()
		skel_attack1 = pygame.image.load('graphics/char/Attack_1.png').convert_alpha()
		skel_attack2 = pygame.image.load('graphics/char/Attack_2.png').convert_alpha()
		skel_attack3 = pygame.image.load('graphics/char/Attack_3.png').convert_alpha()
		skel_hurt = pygame.image.load('graphics/char/Hurt.png').convert_alpha()
		skel_dead = pygame.image.load('graphics/char/dead.png').convert_alpha()
		skel_idle = pygame.image.load('graphics/char/Idle.png').convert_alpha()


		# Skel Walk Animation
		skel_Sheet_width, skel_Sheet_height = skel_walk.get_size()
		skel_width = skel_Sheet_width // skel_walk_frames
		skel_height = skel_Sheet_height

		self.walk_frames = []
		for i in range(skel_walk_frames):
			rect = pygame.Rect(i * skel_width, 0, skel_width, skel_height)
			frame = skel_walk.subsurface(rect)
			frame = pygame.transform.scale(frame, (skel_width * scale_up, skel_height * scale_up))
			self.walk_frames.append(frame)

		#skel attack Animations___________________________________
		skel_Sheet_width2, skel_Sheet_height2 = skel_attack1.get_size()
		skel_width2 = skel_Sheet_width2 // skel_attack_frames
		skel_height2 = skel_Sheet_height2

		self.attack_frames = []
		for i in range(skel_attack_frames):
			rect2 = pygame.Rect(i * skel_width2, 0, skel_width2, skel_height2)
			frame2 = skel_attack1.subsurface(rect2)
			frame2 = pygame.transform.scale(frame2, (skel_width2 * scale_up, skel_height2 * scale_up))
			self.attack_frames.append(frame2)
		#_________________________________________________________
		skel_Sheet_width3, skel_Sheet_height3 = skel_attack2.get_size()
		skel_width3 = skel_Sheet_width3 // skel_attack_frames2
		skel_height3 = skel_Sheet_height3

		self.attack_frames2 =[]
		for i in range(skel_attack_frames2):
			rect3 = pygame.Rect(i * skel_width3, 0, skel_width3, skel_height3)
			frame3 = skel_attack2.subsurface(rect3)
			frame3 = pygame.transform.scale(frame3, (skel_width3 * scale_up, skel_height3 * scale_up))
			self.attack_frames2.append(frame3)
		#_________________________________________________________
		skel_Sheet_width4, skel_Sheet_height3 = skel_attack3.get_size()
		skel_width4 = skel_Sheet_width4 // skel_attack_frames3
		skel_height4 = skel_Sheet_height

		self.attack_frames3 =[]
		for i in range(skel_attack_frames3):
			rect4 = pygame.Rect(i * skel_width4, 0, skel_width4, skel_height4)
			frame4 = skel_attack3.subsurface(rect4)
			frame4 = pygame.transform.scale(frame4, (skel_width4 * scale_up, skel_height4 * scale_up))
			self.attack_frames3.append(frame4)
		#_________________________________________________________
		skel_Sheet_width5, skel_Sheet_height5 = skel_hurt.get_size()
		skel_width5 = skel_Sheet_width5 // skel_hurt_frames
		skel_height5 = skel_Sheet_height5

		self.hurt_frames =[]
		for i in range(skel_hurt_frames):
			rect5 = pygame.Rect(i * skel_width5, 0, skel_width5, skel_height5)
			frame5 = skel_hurt.subsurface(rect5)
			frame5 = pygame.transform.scale(frame5, (skel_width5 * scale_up, skel_height5 * scale_up))
			self.hurt_frames.append(frame5)
		#_________________________________________________________
		skel_Sheet_width6, skel_Sheet_height6 = skel_dead.get_size()
		skel_width6 = skel_Sheet_width6// skel_dead_frames
		skel_height6 = skel_Sheet_height6

		self.dead_frames =[]
		for i in range(skel_dead_frames):
			rect6 = pygame.Rect(i * skel_width6, 0, skel_width6, skel_height6)
			frame6 = skel_dead.subsurface(rect6)
			frame6 = pygame.transform.scale(frame6, (skel_width6 * scale_up, skel_height6 * scale_up))
			self.dead_frames.append(frame6)
		#_________________________________________________________
		skel_Sheet_width7, skel_Sheet_height7 = skel_idle.get_size()
		skel_width7 = skel_Sheet_width7 // skel_idle_frames
		skel_height7 = skel_Sheet_height7

		self.idle_frames =[] 
		for i in range(skel_idle_frames):
			rect7 = pygame.Rect(i * skel_width7, 0, skel_width7, skel_height7)
			frame7 = skel_idle.subsurface(rect7)
			frame7 = pygame.transform.scale(frame7, (skel_width7 * scale_up, skel_height7 * scale_up))
			self.idle_frames.append(frame7)

			self.x_pos = inital_x
			self.y_pos = inital_y

			self.enemy_state = 'idle'
			self.current_eneemy_animation_frames = self.idle_frames
			self.current_enemy_frame_index = 0
			self.enemy_animation_speed = 250
			self.last_frame_time = pygame.time.get_ticks()

			self.is_attacking = False
			self.is_hurt = False
			self.is_dead = False

			self.follow_range = 300
			self.attack_range = 100
			self.movement_speed = 3
			self.health = 50

			self.facing_right = True

			self.original_walk_frames = self.walk_frames[:]
			self.original_attack_frames = self.attack_frames[:]
			self.original_attack_frames2 = self.attack_frames2[:]
			self.original_attack_frames3 = self.attack_frames3[:]
			self.original_hurt_frames = self.hurt_frames[:]
			self.original_dead_frames = self.dead_frames[:]
			self.original_idle_frames = self.idle_frames[:]

			self.attack_damage = 10

			self.attack_active_frames = {'attacking1': [2],'attacking2': [3, 4],'attacking3': [1]}
			self.has_dealt_damage = False

			self.image = self.current_eneemy_animation_frames[self.current_enemy_frame_index]
			self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))


	def update_behavior(self, player_rect):

		if self.is_hurt or self.is_dead or self.is_attacking:
			return

		distance_to_player = math.hypot(self.rect.centerx - player_rect.centerx, self.rect.centery - player_rect.centery)

		if self.rect.centerx < player_rect.centerx:
			self.facing_right = True
		elif self.rect.centerx > player_rect.centerx:
			self.facing_right = False


		if self.enemy_state == 'idle':
			if distance_to_player < self.follow_range:
				self.set_state('walking')

		elif self.enemy_state == 'walking':
			if distance_to_player < self.attack_range:
				attack_choice = random.choice(['attacking1', 'attacking2', 'attacking3'])
				self.set_state(attack_choice)

			elif distance_to_player >= self.follow_range:
				self.set_state('idle')

			else:
				if self.rect.centerx < player_rect.centerx:
					self.x_pos += self.movement_speed
					self.facing_right = True
				elif self.rect.centerx > player_rect.centerx:
					self.x_pos -= self.movement_speed
					self.facing_right = False

				if self.rect.centery < player_rect.centery:
					self.y_pos += self.movement_speed
				elif self.rect.centery > player_rect.centery:
					self.y_pos -= self.movement_speed
					
				min_y = 350
				max_y = 590


				if self.y_pos < min_y:
					self.y_pos = min_y
				elif self.y_pos > max_y:
					self.y_pos = max_y

					self.rect.topleft = (self.x_pos, self.y_pos)	



				


				self.rect.topleft = (self.x_pos, self.y_pos)

		elif self.enemy_state in ('attacking1', 'attacking2', 'attacking3'):
			pass



	def set_state(self, new_state):
		if self.enemy_state != new_state and self.enemy_state != 'dead':
			self.enemy_state = new_state
			self.current_enemy_frame_index = 0
			self.last_frame_time = pygame.time.get_ticks()

			self.is_attacking = False
			self.is_hurt = False
			self.has_dealt_damage = False

		if self.enemy_state == 'idle':
			self.current_eneemy_animation_frames = self.original_idle_frames

		elif self.enemy_state == 'walking':
			self.current_eneemy_animation_frames = self.original_walk_frames

		elif self.enemy_state == 'attacking1':
			self.current_eneemy_animation_frames = self.original_attack_frames
			self.is_attacking = True
			self.has_dealt_damage = False

		elif self.enemy_state == 'attacking2':
			self.current_eneemy_animation_frames = self.original_attack_frames2
			self.is_attacking = True
			self.has_dealt_damage = False

		elif self.enemy_state == 'attacking3':
			self.current_eneemy_animation_frames = self.original_attack_frames3
			self.is_attacking = True
			self.has_dealt_damage = False

		elif self.enemy_state == 'hurt':
			self.current_eneemy_animation_frames = self.original_hurt_frames
			self.is_hurt = True

		elif self.enemy_state == 'dead':
			self.current_eneemy_animation_frames = self.original_dead_frames
			self.is_dead = True

	def take_damage(self, damage):

		if self.enemy_state == 'dead':
			return


		self.health -= damage
		if self.health <= 0:
			self.health = 0
			self.set_state('dead')
		else:
			if self.enemy_state != 'dead':
				self.set_state('hurt')


	def is_attack_hitting(self):
		if self.is_attacking and self.enemy_state in self.attack_active_frames:
			if self.current_enemy_frame_index in self.attack_active_frames[self.enemy_state]:
				if not self.has_dealt_damage:
					return True
		return False

	def notify_damage_dealt(self):
		self.has_dealt_damage = True

	def update(self, player_rect):
		self.update_behavior(player_rect)

		current_time = pygame.time.get_ticks()




		if current_time - self.last_frame_time > self.enemy_animation_speed:
			self.current_enemy_frame_index += 1
			self.last_frame_time = current_time

			if self.current_enemy_frame_index >= len(self.current_eneemy_animation_frames):


				if self.enemy_state in ('attacking1', 'attacking2', 'attacking3'):
					self.is_attacking = False
					self.current_enemy_frame_index = 0
					self.has_dealt_damage = False
					self.set_state('idle')


				elif self.enemy_state == 'hurt':
					self.is_hurt = False
					self.current_enemy_frame_index = 0

					if self.health <= 0:
						self.set_state('dead')
					else:
						self.set_state('idle')

				elif self.enemy_state =='dead':

					self.current_enemy_frame_index = len(self.current_enemy_animation_frames) - 1
					self.is_dead = True

				else:
					self.current_enemy_frame_index %= len(self.current_eneemy_animation_frames)

		if self.current_eneemy_animation_frames:
			self.image = self.current_eneemy_animation_frames[self.current_enemy_frame_index]

			if not self.facing_right:
				self.image = pygame.transform.flip(self.image, True, False)
	





