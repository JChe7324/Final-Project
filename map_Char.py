import pygame
import os

class MapCharacter(pygame.sprite.Sprite):
    def __init__(self, start_pos_on_map_image):
        super().__init__()

        num_frames = 6
        scale_up = 2

        
        man_walk = pygame.image.load('graphics/char/d_walk.png').convert_alpha()


        sheet_width, sheet_height = man_walk.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height

        self.frames = []
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = man_walk.subsurface(frame_rect)
            frame = pygame.transform.scale(frame, (frame_width * scale_up, frame_height * scale_up))
            self.frames.append(frame)

        self.current_frame_index = 0
        self.animation_speed = 150
        self.last_frame_time = pygame.time.get_ticks()

        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(center=(start_pos_on_map_image))


    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame_time > self.animation_speed:
            self.current_frame_index += 1
            self.last_frame_time = current_time

            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0

            current_center = self.rect.center
            self.image = self.frames[self.current_frame_index]
            self.rect = self.image.get_rect(center=current_center)

            