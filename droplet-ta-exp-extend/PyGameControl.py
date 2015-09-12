# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 13:17:50 2015

@author: Colab
"""
import math
import pygame
from pygame.locals import *

import RobotData
import FireData

DEFAULT_FPS = 60
COLOR_GRAY = (100, 100, 100)

class PyGameControl:
    def __init__(self, title, experiment_number, screen_x, screen_y, fps=DEFAULT_FPS):
        """
        Initializes pygame user input and rendering class
        """
        self.fps = fps
        self.title = title
        self.screen_x = screen_x
        self.screen_y = screen_y        
        self.exp_num = experiment_number
        
    def setup(self):
        """
        Sets up pygame stuff
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y), HWSURFACE | DOUBLEBUF)
        pygame.display.set_caption(self.title + '. Exp. #' + str(self.exp_num))
        self.clock = pygame.time.Clock()
        self.screen.fill((0,0,0))
        
    def handle_user_events(self):
        """
        Uses the PyGame event handler to handle user inputs. Returns a 
        list of observed events possibly with added metadata.
        """
        # Get user input and data from pygame
        ret_str_list = []
        for event in pygame.event.get():
            # keydown events go here
            if event.type == QUIT:
                ret_str_list.append('exit')
                break
                
            elif event.type == MOUSEBUTTONUP:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                # Left click add fire source
                if event.button == 1:
                    ret_str_list.append(('left-mouse-click',(mouse_x, mouse_y)))
                # Right click extinguishes an entire fire "blob" area
                elif event.button == 3:
                    ret_str_list.append(('right-mouse-click',(mouse_x, mouse_y)))

            elif event.type == pygame.KEYDOWN:
                # Pressing the 'o' kay starts an optimization thread
                if event.key == pygame.K_o:
                    self._launch_opt_thread()
            
        return ret_str_list
        
    def draw_fire(self, fire_data_list, scale_to_screen=None):
        for fdat in fire_data_list:
            if scale_to_screen is not None:
                (scale_x, scale_y) = scale_to_screen
                (px_x, px_y) = self._scale(fdat.x, fdat.y, scale_x, scale_y)
                (r_w, r_h) = self._scale(fdat.radius, fdat.radius, scale_x, scale_y)
                
                ellipse_rect = pygame.Rect(0,0,r_w,r_h)
                ellipse_rect.center(px_x, px_y)
                
                # draw stuff
            else:
                pygame.draw.circle(screen, fdat.color, (fdat.x, fdat.y), fdat.radius)
    
    def draw_robots(self, robot_data_list, scale_to_screen=None):
        # Draw robots to screen
        for rdat in robot_data_list:
            if scale_to_screen is not None:
                (scale_x, scale_y) = scale_to_screen
                (px_x, px_y) = self._scale(rdat.x, rdat.y, scale_x, scale_y)
                (r_w, r_h) = self._scale(rdat.simonly_radius, rdat.simonly_radius, scale_x, scale_y)

                ellipse_rect = pygame.Rect(0,0,r_w,r_h)
                ellipse_rect.center(px_x, px_y)

                pygame.draw.ellipse(screen, rdat.simonly_color, ellipse_rect, rdat.simonly_radius - 1) 
                pygame.draw.ellipse(screen, COLOR_GRAY, ellipse_rect, rdat.simonly_radius - 1) 
                pygame.draw.line(screen, rdat.simonly_color, (px_x, px_y), (px_x + int(r_w * math.cos(rdat.orient_rad())), px_y + int(r_h * math.sin(rdat.orient_rad()))))

            else:
                pygame.draw.circle(screen, rdat.simonly_color, (rdat.x, rdat.y), rdat.simonly_rad, 1)
                pygame.draw.circle(screen, COLOR_GRAY, (rdat.x, rdat.y), rdat.simonly_rad - 1) 
                pygame.draw.line(screen, rdat.simonly_color, (rdat.x, rdat.y), (rdat.x + int(rdat.simonly_rad * math.cos(rdat.orient_rad())), rdat.y + int(rdat.simonly_rad * math.sin(rdat.orient_rad()))))              
            
    
    def render(self, fps_lock=True):
        """
        Call this function after all the draw_@@@ calls to render draw elements
        to screen
        """
        # Render to self.screen
        pygame.display.flip()
        if fps_lock:
            self.clock.tick(self.fps)        
        else:
            self.clock.tick()    
            
    def _scale(self, x, y, scale_x, scale_y):
        return (x * self.screen_x / float(scale_x), y * self.screen_y / float(scale_y))
        
        
        