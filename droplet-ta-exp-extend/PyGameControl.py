# -*- coding: utf-8 -*-
import math
import pygame
import pygame.locals

DEFAULT_FPS = 60
RGB_GRAY  = (100, 100, 100)
RGB_BLACK = (0,   0,   0)
RGB_WHITE = (255, 255, 255)

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
        
    def init(self):
        """
        Sets up pygame stuff
        """
        pygame.init()
        self.pg_font = pygame.font.SysFont('monospace', 10)
        self.pg_font.set_bold(True)
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y), pygame.locals.HWSURFACE | pygame.locals.DOUBLEBUF)
        pygame.display.set_caption(self.title + '. Exp. #' + str(self.exp_num))
        self.clock = pygame.time.Clock()
        self.screen.fill(RGB_BLACK)
        
    def handle_user_events(self):
        """
        Uses the PyGame event handler to handle user inputs. Returns a 
        list of observed events possibly with added metadata.
        """
        # Get user input and data from pygame
        ret_str_list = []
        for event in pygame.event.get():
            # keydown events go here
            if event.type == pygame.locals.QUIT:
                ret_str_list.append('exit')
                break
                
            elif event.type == pygame.locals.MOUSEBUTTONUP:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                # Left click add fire source
                if event.button == 1:
                    ret_str_list.append(('left-mouse-click',(mouse_x, mouse_y)))
                # Right click extinguishes an entire fire "blob" area
                elif event.button == 3:
                    ret_str_list.append(('right-mouse-click',(mouse_x, mouse_y)))

            elif event.type == pygame.KEYDOWN:
                # Pressing the 'o' kay starts an optimization thread
                if event.key == pygame.K_l:
                    ret_str_list.append(('key-down', 'l'))
            
        return ret_str_list
        
    def draw_fire(self, fire_data_list, scale_to_screen=None):
        for fdat in fire_data_list:
            if scale_to_screen is not None:
                (scale_x, scale_y) = scale_to_screen
                (px_x, px_y) = self._scale(fdat.x, fdat.y, scale_x, scale_y)
                (r_w, r_h) = self._scale(2*fdat.radius, 2*fdat.radius, scale_x, scale_y)
                
                # Draw fire
                ellipse_rect = pygame.Rect(0,0,r_w,r_h)
                ellipse_rect.center = (px_x, px_y)                
                pygame.draw.ellipse(self.screen, fdat.color(), ellipse_rect)
                
                # Draw text
                textbox = self.pg_font.render(str(fdat.intensity), True, RGB_WHITE, fdat.color())
                textbox_pos = textbox.get_rect()
                textbox_pos.center = ellipse_rect.center
                self.screen.blit(textbox, textbox_pos)
                
            else:
                # Draw fire
                pygame.draw.circle(self.screen, fdat.color(), (fdat.x, fdat.y), int(fdat.radius))
                
                # Draw text
                textbox = self.pg_font.render(str(fdat.intensity), True, RGB_WHITE, fdat.color())
                textbox_pos = textbox.get_rect()
                textbox_pos.center = (fdat.x, fdat.y)
                self.screen.blit(textbox, textbox_pos)                
    
    def draw_robots(self, robot_data_list, scale_to_screen=None):
        """
        Draws robots to screen. scale_to_screen is a scaling tuple 
        (arena_x, arena_y) between arena and screen coordinates, if required. 
        """
        for rdat in robot_data_list:
            if scale_to_screen is not None:
                (scale_x, scale_y) = scale_to_screen
                (px_x, px_y) = self._scale(rdat.x, rdat.y, scale_x, scale_y)
                (r_w, r_h) = self._scale(2*rdat.simonly_radius, 2*rdat.simonly_radius, scale_x, scale_y)

                # Draw robot
                ellipse_rect = pygame.Rect(0,0,r_w,r_h)
                ellipse_rect.center = (px_x, px_y)
                pygame.draw.ellipse(self.screen, rdat.simonly_color, ellipse_rect, 1)
                ellipse_rect.height -= 1
                ellipse_rect.width -= 1
                pygame.draw.ellipse(self.screen, RGB_GRAY, ellipse_rect)
                pygame.draw.line(self.screen, rdat.simonly_color, (px_x, px_y), (px_x + int((r_w/2)* math.cos(math.radians(rdat.orient))), px_y + int((r_h/2) * math.sin(math.radians(rdat.orient)))))

                # Draw text
                textbox = self.pg_font.render(str(rdat.robot_id), True, RGB_BLACK, RGB_GRAY)
                textbox_pos = textbox.get_rect()
                textbox_pos.center = ellipse_rect.center
                self.screen.blit(textbox, textbox_pos)
                
            else:
                # Draw Robot
                (px_x, px_y) = (int(rdat.x), int(rdat.y))
                pygame.draw.circle(self.screen, rdat.simonly_color, (px_x, px_y), rdat.simonly_radius, 2)
                pygame.draw.circle(self.screen, RGB_GRAY, (px_x, px_y), rdat.simonly_radius - 2) 
                pygame.draw.line(self.screen, rdat.simonly_color, (px_x, px_y), (px_x + int(rdat.simonly_radius * math.cos(math.radians(rdat.orient))), px_y + int(rdat.simonly_radius * math.sin(math.radians(rdat.orient)))))
            
                # Draw text
                textbox = self.pg_font.render(str(rdat.robot_id), True, RGB_BLACK, RGB_GRAY)
                textbox_pos = textbox.get_rect()
                textbox_pos.center = (rdat.x, rdat.y)
                self.screen.blit(textbox, textbox_pos)
                
    def render(self, fps_lock=True):
        """
        Call this function after all the draw_### calls to render draw elements
        to screen
        """
        # Render to self.screen
        pygame.display.flip()
        if fps_lock:
            self.clock.tick(self.fps)        
        else:
            self.clock.tick()
            
        self.screen.fill(RGB_BLACK)
    
    def quit(self):
        return pygame.quit()
    
    def _scale(self, x, y, scale_x, scale_y):
        return (int(x * self.screen_x / float(scale_x)), int(y * self.screen_y / float(scale_y)))