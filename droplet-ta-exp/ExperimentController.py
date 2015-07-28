# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:48:54 2015

@author: Anshul
"""
import pygame
import threading
from pygame.locals import *
from FireController import FireController
from TASolver import TASolver
from Estimator import Estimator

USING_SERIAL = True
if USING_SERIAL:
    from SerialInterface import SerialInterface

# Set to True when RoboRealm is in use
USING_RR = True
if USING_RR:
    from RoboRealmInterface import RoboRealmInterface

class ExperimentController:

    def __init__(self, title, fps, screen_x, screen_y, cell_w, cell_h):
        self.title = title
        self.fps = fps
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.timer_counter = 0
        self.active_threads = []
        self.robot_assignment_matrix = None
        self.utility_vector = None
        self.num_start_fires = 4
        
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
        for _ in range(self.num_start_fires):
            (retval, state) = self.fm.ignite_cell_random()        
            if not retval:
                return False
            
        # Set up the RoboRealm interface
        if USING_RR:
            self.rri = RoboRealmInterface()
            self.rri.connect()

            # Set up the Estimator class
            self.est = Estimator(self.screen_x, self.screen_y, self.rri.rr_x, self.rri.rr_y)
        
        # Set up Serial Interface
        if USING_SERIAL:
            self.serial_port = SerialInterface()        
            if not self.serial_port.open('COM16'):
                return False
            
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
                if USING_SERIAL:
                    self.serial_port.close()
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
                    self._launch_opt_thread()
            
        return ret_str_list
                    
    def handle_timed_events(self):
        """
        Handle events that happen at regularly timed intervals
        """
        # 1 second interval
        if (self.timer_counter % (self.fps * 1)) == 0:
            self._fire_positions = self.fm.get_fire_locations_and_sizes()
            if USING_RR:
                self._robot_postions = self.rri.get_robot_positions()

        # 5 second interval
        if (self.timer_counter % (self.fps * 5)) == 0:
            if self.robot_assignment_matrix is not None and USING_SERIAL:
                self.est.set_current_assignments(self.robot_assignment_matrix)
                (robot_action_list, completed_targets) = self.est.compute_robot_action_list(self._fire_positions, self._robot_postions)
                self.serial_port.write(robot_action_list)
                for completed_target in completed_targets:
                    (col, row) = completed_target
                    self.fm.extinguish_fire(row, col)
                               

        # 10 second interval
        if (self.timer_counter % (self.fps * 10)) == 0:
            pass

        # 20 second interval
        if (self.timer_counter % (self.fps * 20)) == 0:
            pass

        # 30 second interval
        if (self.timer_counter % (self.fps * 30)) == 0:
            self.fm.increment_intensity(16)
            self._launch_opt_thread()
    
        # 1 minute interval
        if (self.timer_counter % (self.fps * 60)) == 0:
            pass
             
        # 2 minute interval
        if (self.timer_counter % (self.fps * 120)) == 0:
            pass

        # 10 minute interval
        if (self.timer_counter % (self.fps * 600)) == 0:
            if not self.fm.ignite_cell_random():
                print('Error while creating a new fire. Terminating.')
                return False
            self.timer_counter = 0
             
        # Every time-step of the experiment
        # Check if any running threads have finished
        if (len(self.active_threads) > 0):
            new_active_threads = []
            for thread in self.active_threads:
                if not thread.is_alive():
                    (self.robot_assignment_matrix, self.utility_vector) = self._tasolver.get_solution()
                    print self.robot_assignment_matrix
                else:
                    new_active_threads.append(thread)
            self.active_threads = new_active_threads

        # Propogate the fire
        self.fm.propogate_fire()

        # update the timer
        self.timer_counter += 1
        
        return True
        
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
        
    def _launch_opt_thread(self):
        """
        Uses the TASolver class to run an optimial target assignment routine.
        """
        self._tasolver = TASolver()

        # Assign opt variables here
        num_robots = len(self._robot_postions)
        num_targets = len(self._fire_positions)
        target_team_size_req = self.est.estimate_required_team_sizes(self._fire_positions)
        target_payoffs = [((x,y), 1) for ((x,y), _) in self._fire_positions]
        robot_constraints = self.est.estimate_robot_constraints(self._fire_positions, self._robot_postions)
        
        new_thread = threading.Thread(target=self._tasolver.solve, kwargs=dict(n=num_robots, t=num_targets, k=target_team_size_req, w=target_payoffs, cst=robot_constraints))
        self.active_threads.append(new_thread)
        new_thread.start()