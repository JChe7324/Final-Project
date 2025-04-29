import pygame
from sys import exit
import os
import math
import random
from character_for_kingdom import Character
from skel_for_kingdom import Enemy
from map_Char import MapCharacter
from pygame.math import Vector2


def main():
	pygame.init()
	screen = pygame.display.set_mode((1400,800))
	pygame.display.set_caption('Kingdom Fall Trail')
	clock = pygame.time.Clock()

	map_surfaces = {
        'map1': pygame.transform.scale(pygame.image.load('graphics/Mockup1.png').convert_alpha(), (screen.get_width(), screen.get_height())),
        'map2': pygame.transform.scale(pygame.image.load('graphics/Mockup2.png').convert_alpha(), (screen.get_width(), screen.get_height())),
        'map3': pygame.transform.scale(pygame.image.load('graphics/Mockup3.png').convert_alpha(), (screen.get_width(), screen.get_height())),
    }
	current_map_key = 'map1'

	map_rect = map_surfaces[current_map_key].get_rect(topleft=(0, 0))

	map_points = {
        'map1': [
            (100, 150), (250, 200), (400, 180), (550, 250), (700, 300)
        ],
        'map2': [
            (50, 50), (180, 100), (300, 150), (450, 120)
        ],
        'map3': [
            (100, 100), (200, 50), (300, 100), (400, 150), (500, 100)
        ]
    }

	map_connections = {
        ('map1', 4): ('map2', 0),
        ('map2', 3): ('map3', 0),
    }


	initial_map_marker_pos = map_points[current_map_key][0]
	map_marker_pos = Vector2(initial_map_marker_pos)
	current_map_point_index = 0
	target_map_point_index = 0
	map_marker_speed = 0.5
	is_marker_moving = False

	map_character_sprite = MapCharacter(initial_map_marker_pos)
	map_character_group = pygame.sprite.Group(map_character_sprite)


	ground_surface = pygame.image.load('graphics/ground.jpg').convert_alpha()
	ground_width = ground_surface.get_width()
	ground_height = ground_surface.get_height()


	game_state = 'map_view'


	distance_traveled = 0
	food = 500
	health = 50
	gold = 200
	current_location_name = 'Starting Point'
	travel_speed = 100
	event_chance = 1.0

	event_history = []
	max_event_message = 5 


	background_scroll_x = 0
	background_scroll_speed = 1


	ui_box_rect = pygame.Rect(10,screen.get_height() - 200 ,250,200)
	UI_GREY = (128, 128, 128)
	semi_grey = (128, 128, 128, 128)

	ui_surface = pygame.Surface((ui_box_rect.width, ui_box_rect.height), pygame.SRCALPHA)

	ui_surface.fill(semi_grey)

	font = pygame.font.Font(None, 24)


	character = Character(700, 500)
	character.health = health

	enemy = None
	
	player_group = pygame.sprite.Group(character)
	enemy_group = pygame.sprite.Group()


	while True:
		dt = clock.tick(60) / 1000

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN:
				if game_state == 'combat':
					if event.key == pygame.K_SPACE:
						character.start_attack()

				elif game_state == 'map_view':
					if event.key == pygame.K_SPACE and not is_marker_moving:
						current_map_point_index = target_map_point_index
						num_points_on_current_map = len(map_points[current_map_key])
						next_point_index_candidate = (current_map_point_index + 1) % num_points_on_current_map

						connection = map_connections.get((current_map_key, next_point_index_candidate))

						if connection:
							next_map_key, entry_point_on_new_map_index = connection
							current_map_key = next_map_key
							target_map_point_index = entry_point_on_new_map_index
							map_rect = map_surfaces[current_map_key].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
							map_marker_pos = list(map_points[current_map_key][target_map_point_index])
							is_marker_moving = False
							event_triggered_for_point = False
							print("Reached connection. Moved to map:", current_map_key, "starting at point", target_map_point_index)

						else:
							target_map_point_index = next_point_index_candidate
							is_marker_moving = True
							event_triggered_for_point = False
							print("Marker moving on", current_map_key, "from point", current_map_point_index, "to point", target_map_point_index)
				
				elif game_state in ['traveling', 'resting']:
					if event.key == pygame.K_m:
						game_state = 'map_view'
						print("Viewing Map")



		keys = pygame.key.get_pressed()

		if game_state == 'map_view':

			marker_screen_pos_center = (map_rect.x + map_marker_pos[0], map_rect.y + map_marker_pos[1])
			map_character_sprite.rect.center = marker_screen_pos_center
			map_character_group.update()

			if is_marker_moving:
				start_pos = Vector2(map_marker_pos)
				end_pos = Vector2(map_points[current_map_key][target_map_point_index])

				if start_pos.distance_to(end_pos) > 0.1:
					direction = (end_pos - start_pos).normalize()
					move_distance = map_marker_speed * dt * 60
					map_marker_pos += direction * move_distance

					if start_pos.distance_to(end_pos) <= move_distance:
						map_marker_pos = Vector2(end_pos)
						is_marker_moving = False
						event_triggered_for_point = False
						print("Marker reached point", target_map_point_index, "on", current_map_key)

						if not event_triggered_for_point:
							distance_traveled += 10

							current_location_name = "Point " + str(target_map_point_index + 1)

							event_type = random.choice(['bandit_attack', 'find_food', 'illness', 'nothing'])

							event_message = "Event at " + str(current_location_name)
							if event_type == "bandit_attack":
								game_state = 'combat'
								print("Entering Combat")
								enemy = Enemy(character.x_pos + 300 * (-1 if character.facing_right else 1), character.y_pos)
								enemy_group.add(enemy)
								

							elif event_type == 'find_food':
								amount_found = random.randint(10, 50)
								food += amount_found
								print("Found food! we now have", food, "food left")
								game_state = 'traveling'
								print("Returning to Traveling view")
								

							elif event_type == 'illness':
								damage_taken = random.randint(5, 20)
								character.take_damage(damage_taken)
								print("I got sick! player health is now", character.health)
								game_state = 'traveling'
								print("Returning to Traveling view")
								

							elif event_type == 'nothing':
								print("Nothing happened.")
								game_state = 'traveling'
								

							event_triggered_for_point = True



		elif game_state == 'traveling' or game_state == 'resting':
			player_group.update(keys)



			if game_state == 'traveling':
				food -= 0.05 * dt
				if food < 0: food = 0


			elif game_state == 'resting':
				food -= 0.2 * dt
				if food < 0: food = 0
				if character.health < 100:
					character.health += 0.5 * dt * 60
					if character.health > 100: character.health = 100


		elif game_state == 'combat':
			if not character.is_hurt and not character.is_dead:
				character.update_postions(keys)
				character.update(keys)

			if enemy_group:
			    enemy_group.update(character.rect)

			if hasattr(character, 'is_attack_hitting') and character.is_attack_hitting():
				collided_enemies = pygame.sprite.spritecollide(character, enemy_group, False)
				for enemy_sprite in collided_enemies:
					enemy_sprite.take_damage(character.attack_damage)
					if hasattr(character, 'notify_damage_dealt'):
						character.notify_damage_dealt()

			for enemy_sprite in enemy_group:
				if hasattr(enemy_sprite, 'is_attack_hitting') and enemy_sprite.is_attack_hitting():
					if pygame.sprite.collide_rect(enemy_sprite, character):
						character.take_damage(enemy_sprite.attack_damage)
						if hasattr(enemy_sprite, 'notify_damage_dealt'):
							enemy_sprite.notify_damage_dealt()

			if enemy_group and all(enemy_sprite.health <= 0 for enemy_sprite in enemy_group):
				game_state = 'map_view'
				print("You beat the Bandit, returning to Map view")
				map_marker_pos = list(map_points[current_map_key][target_map_point_index])
				is_marker_moving = False
				event_triggered_for_point = False
				enemy_group.empty()

			if character.health <= 0:
				game_state = 'game_over'
				print("Game Over!")


		elif game_state == 'game_over':
			pass


		screen.fill((0, 0, 0))

		if game_state == 'map_view':
			screen.blit(map_surfaces[current_map_key], map_rect)
			map_character_group.draw(screen)

		elif game_state == 'traveling' or game_state == 'resting':
			screen.blit(ground_surface, (background_scroll_x, -200))
			screen.blit(ground_surface, (background_scroll_x + ground_width, -200))
			player_group.draw(screen)

		elif game_state in ['combat']:
			screen.blit(ground_surface, (0, -200))
			player_group.draw(screen)
			enemy_group.draw(screen)

		elif game_state == 'game_over':
			game_over_text_surface = font.render("Game Over!", True, (255, 0, 0))
			game_over_rect = game_over_text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
			screen.blit(game_over_text_surface, game_over_rect)



		if game_state in ['traveling', 'resting', 'combat', 'map_view', 'game_over']:

			screen.blit(ui_surface, ui_box_rect.topleft)

			current_health = character.health
			current_distance = int(distance_traveled)
			current_food = int(food)
			current_gold = gold
			current_state = game_state.capitalize()
			current_map_name = current_map_key.replace('_', ' ').title()
			current_location_name = "Point " + str(target_map_point_index + 1)

			TEXT_COLOR = (255, 255, 255)

			distance_text_string = "Distance: " + str(current_distance) + " miles"
			food_text_string = "Food: " + str(current_food)
			health_text_string = "Health: " + str(current_health)
			gold_text_string = "Gold: " + str(current_gold)
			state_text_string = "State: " + str(current_state)
			map_text_string = "Map: " + str(current_map_name)
			location_text_string = "Location: " + str(current_location_name)

			font = pygame.font.Font(None, 24)
			distance_surface = font.render(distance_text_string, True, TEXT_COLOR)
			food_surface = font.render(food_text_string, True, TEXT_COLOR)
			health_surface = font.render(health_text_string, True, TEXT_COLOR)
			gold_surface = font.render(gold_text_string, True, TEXT_COLOR)
			state_surface = font.render(state_text_string, True, TEXT_COLOR)
			map_surface_text = font.render(map_text_string, True, TEXT_COLOR)
			location_surface_text = font.render(location_text_string, True, TEXT_COLOR)

			padding_x = 10
			padding_y = 10
			line_height = font.get_linesize() + 2

			screen.blit(distance_surface, (ui_box_rect.x + padding_x, ui_box_rect.y + padding_y))
			screen.blit(food_surface, (ui_box_rect.x + padding_x, ui_box_rect.y + padding_y + line_height))
			screen.blit(health_surface, (ui_box_rect.x + padding_x, ui_box_rect.y + padding_y + line_height * 2))
			screen.blit(gold_surface, (ui_box_rect.x + padding_x, ui_box_rect.y + padding_y + line_height * 3))
			screen.blit(state_surface, (ui_box_rect.x + padding_x, ui_box_rect.y + padding_y + line_height * 4))
			screen.blit(map_surface_text, (ui_box_rect.x + padding_x, ui_box_rect.y + padding_y + line_height * 5))
			screen.blit(location_surface_text, (ui_box_rect.x + padding_x, ui_box_rect.y + padding_y + line_height * 6))

			event_history_start_y = ui_box_rect.y + padding_y + line_height * 7
			for i, event_msg in enumerate(event_history):
					event_surface = font.render(event_msg, True, TEXT_COLOR)
					screen.blit(event_surface, (ui_box_rect.x + padding_x, event_history_start_y + i * line_height))


		pygame.display.update()


main()