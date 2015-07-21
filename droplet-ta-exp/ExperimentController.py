# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:48:54 2015

@author: Anshul
"""
import pygame
from pygame.locals import *
from FireController import *
from TASolver import *
from RoboRealmInterface import *
import copy

class ExperimentController:

    def __init__(self, title, fps, screen_x, screen_y, cell_w, cell_h):
        self.title = title
        self.fps = fps
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.timer_counter = 0
        self._active_threads = []
        
    def setup_experiment(self):        
        """
        Sets up the required classes for the experiment
        """
        # Set up PyGame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y), HWSURFACE | DOUBLEBUF)
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.screen.fill((0,0,0))
        
        # Set up FireController
        self.fm = FireController(self.screen_y / self.cell_h, self.screen_x / self.cell_w)
        (retval, state) = self.fm.ignite_cell_random()              
        if not retval:
            print('Problem initializing fire grid.')
            return False
            
        # Set up the RoboRealm interface
        self.rri = RoboRealmInterface()
        self.rri.connect()
            
        return True
            
    def handle_user_events(self):
        """
        Uses the PyGame event handler to handle user inputs. Returns a string 
        """
        # Get user input and data from roborealm
        ret_str_list = []
        for event in pygame.event.get():
            # keydown events go here
            if event.type == QUIT:
                pygame.quit()
                ret_str_list.append('exit')
                break
                
            elif event.type == MOUSEBUTTONUP:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                # Left click add fire source
                if event.button == 1:
                    self.fm.ignite_cell(mouse_y/self.cell_h, mouse_x/self.cell_w)
                    ret_str_list.append('left-mouse-click')
                # Right click extinguishes an entire fire "blob" area
                elif event.button == 3:
                    self.fm.extinguish_fire(mouse_y/self.cell_h, mouse_x/self.cell_w)
                    ret_str_list.append('right-mouse-click')

            elif event.type == pygame.KEYDOWN:
                # Pressing the 'o' kay starts an optimization thread
                if event.key == pygame.K_o:
                    self.launch_opt_thread()
            
        return ret_str_list
                    
    def handle_timed_events(self):
        """
        Handle events that happen at regularly timed intervals
        """
        # Minute interval
        if self.timer_counter > (self.fps * 60):
            self.timer_counter = 1
                
        # 20 second interval
        if (self.timer_counter % (self.fps * 20)) == 0:
            self.fm.increment_intensity(5)

        # 10 second interval
        if (self.timer_counter % (self.fps * 10)) == 0:
            pass
        
        # 5 second interval
        if (self.timer_counter % (self.fps * 5)) == 0:
            print self.rri.get_robot_positions()
        
        
        # Every time-step of the experiment
        # Check if any running threads have finished
        if (len(self._active_threads) > 0):
            for thread in self._active_threads:
                if not thread.is_active():
                    # Get thread related computation results out here
                    self._active_threads.remove(thread)
                    
        # Propogate the fire
        self.fm.propogate_fire()               

        # update the timer
        self.timer_counter += 1
        
    def draw_and_wait(self):
        """
        Draws required information to the screen or projector and waits to
        maintain a consistent frame rate
        """
        # Draw the fire
        diff_fire_grid_dict = self.fm.get_fire_grid()
        
        for (y_pos, x_pos), (intensity, status) in diff_fire_grid_dict.iteritems():
            cell_color = (0,0,0) # (r,g,b)
            if status==FireController.Cell.FRONT:
                cell_color = (0,0,255)
            elif status==FireController.Cell.CORE:
                cell_color = (255, 255 - intensity, 0)               
            elif status==FireController.Cell.BURNT:
                cell_color = (180, 180, 180)                
            self.screen.fill(cell_color, pygame.Rect((x_pos * self.cell_w, y_pos * self.cell_h), (self.cell_w, self.cell_h)))
        
        # Render to self.screen
        pygame.display.flip()
        self.clock.tick(self.fps)
        
    def launch_opt_thread(self):
        """
        Uses the TASolver class to run an optimial target assignment routine.
        
        """
        self._tasolver = TASolver()

        # Assign opt variables here
        fire_loc_and_size = self.fm.get_fire_locations_and_sizes()
        num_robots = 20
        num_targets = len(fire_loc_and_size)
        target_team_size_req = [5 for _ in len(num_targets)]
        target_payoffs = [1 for _ in len(num_targets)]
        robot_constraints = []
        
        new_thread = Thread(target=self._tasolver.solve, kwargs=dict(n=num_robots, t=num_targets, k=target_team_size_req, w=target_payoffs, cst=robot_constraints))
        self._active_threads.append(new_thread)
        new_thread.start()
        
    