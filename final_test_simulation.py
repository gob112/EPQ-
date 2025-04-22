import gym
from gym import spaces
import numpy as np
import pygame
import random
from final_test_sim2 import Road_direction
from stable_baselines3 import PPO
import csv
import os




road_width = 90
stop_line_length = 45  # Length of the stop lines
line_thickness = 5
WIDTH = 1000
HEIGHT = 1000
stop_line_bottom =  HEIGHT // 2 +50
stop_line_top = HEIGHT // 2 -80
stop_line_right = WIDTH//2 +50
stop_line_left = WIDTH//2 -80
CELL_WIDTH = 90
CELL_HEIGHT = 30
PADDING = 6 

class TrafficLighAi(gym.Env):
    metadata = {"render.mode":["human"]}
    def __init__(self):
        super(TrafficLighAi,self).__init__()
        # self.action_space=spaces.MultiBinary(4)
        self.action_space = spaces.MultiDiscrete([3, 3])
        self.observation_space=spaces.Box(
            low=0,high=100,shape=(8,),dtype=np.float32
        )
        self.width = 1000
        self.height = 1000
        self.car_speed = 0.05
        self.road_width = 90
        self.bufferU = 1000
        self.bufferL = 1000
        self.righ_left = Road_direction("right_left")
        self.up_down = Road_direction("up_down")
        self.trafficlight = self.initialize_trafficlight()
        self.screen = None
        self.running = False
        self.total_cars_passed = 0
        self.total_cars_stoped= 0
        self.timings = [["Traffic1","Traffic2","Traffic3","Traffic4"]]
        self.total_reward = 0
        self.negetive_reward = 0
        self.frame=0
        self.f=open("random_number.txt","r")
        
    def initialize_trafficlight(self):
        left_light,righ_light = self.righ_left.make_traffic_light()
        up_light,down_light = self.up_down.make_traffic_light()
        
        return [left_light,righ_light,up_light,down_light]
    def reset(self):
        self.frame = 0
        self.up_down.c = []
        self.righ_left.c = []
        self.total_cars_passed = 0
        self.negetive_reward=0
        for light in self.trafficlight:
            if light.direc =="l" or light.direc == "r":
                light.colour = "green"
                light.green_duration = 3000
                light.red_duration = 3000
            elif light.direc =="u" or light.direc == "d":
                light.colour = "red"
                light.green_duration = 3000
                light.red_duration = 3000
    
        
       
    
        return self.get_obs()
    def get_obs(self):
        
        # u = 0
        # d = 0
        # for car in self.up_down.c:
        #     if car.direction == "u" and car.y > stop_line_bottom:
        #         u+=1
                
        #     elif car.direction == "d" and car.y < stop_line_top:
        #         d +=1
        cu = 0
        cr = 0
        cl = 0
        cd = 0
        tr = []
        for cars in self.up_down.c:
            if cars.direction == "u":
                cu +=1
            elif cars.direction == "d":
                cd +=1
        for cars in self.righ_left.c:
            if cars.direction == "l":
                cl+=1
            elif cars.direction == "r":
                cr+=1
        for t in self.trafficlight:
            if t.colour =="red":
                tr.append(1)
            elif t.colour == "green":
                tr.append(0)
        return np.array([cu,cd,cl,cr]+tr,dtype = np.float32)
    def step(self,action):
        # done = False
        u = []
        l = []
        Pu=Pl=0
        
        # reward = 0
        if self.trafficlight[2].colour=="green":
            for car in self.up_down.c:
                if car.direction == "u" and car.y == stop_line_bottom:
                    if car not in u:
                        u.append(car)
                    
                if car.direction == "d" and car.y == stop_line_top:
                    if car not in u:
                        u.append(car)
                        
                
              
        
        stop_up = self.trafficlight[2].stop_or_not()
        stop_right = self.trafficlight[1].stop_or_not()
            
       
            
        if self.trafficlight[0].colour=="green":
            for car in self.righ_left.c:
                if car.direction == "r" and car.x == stop_line_right:
                    if car not in l:
                        l.append(car)
              
                if car.direction == "l" and car.x ==stop_line_left:
                    if car not in l:
                       l.append(car) 
            
        self.total_cars_passed += (len(u)+len(l))
        Pu = sum(
        1 for v in self.up_down.c if not v.lines_passed and ((v.direction == "u" and v.y >= WIDTH // 2 + 85 and stop_up) or
                                                            (v.direction == "d" and v.y <= WIDTH // 2 - 100 and stop_up))
        )

        Pl = sum(
            1 for v in self.righ_left.c if not v.lines_passed and ((v.direction == "l" and v.x >= WIDTH // 2 + 100 and stop_right) or
                                                            (v.direction == "r" and v.x <= WIDTH // 2 - 100 and stop_right))
        )
            
        
        ch = False
        if self.bufferU>=1000 and self.bufferL >=1000:
            self.trafficlight[0].update_timer()
            self.trafficlight[2].update_timer()
       
        if self.trafficlight[0].should_change():
         
            if self.trafficlight[0].colour == "red":
                if self.bufferL > 0:
                    
                    self.bufferL -= 1  
                else:
              
                    self.trafficlight[0].change()
                    self.trafficlight[1].change()
                    ch =True
                    self.bufferL = 1000
                    
            else:  
               
                self.trafficlight[0].change()
                self.trafficlight[1].change()
                self.bufferL = 1000
                # ch =True
                
        if self.trafficlight[2].should_change():
            
            if self.trafficlight[2].colour == "red":
  
                if self.bufferU > 0:
                    
                    self.bufferU -= 1  
                else:
                    self.trafficlight[2].change()
                    self.trafficlight[3].change()
                    self.bufferU = 1000
                    ch =True
                    
            else:  
                self.trafficlight[2].change()
                self.trafficlight[3].change()
                self.bufferU = 1000
                # ch =True
                
        reward = 0
        done = False
       
       
        if ch:
            
            scaling_factor = 1.1
            if action[0] == 1:  # Increase up-down green duration
                self.trafficlight[2].green_duration *= scaling_factor
            elif action[0] == 2:  # Decrease up-down green duration
                self.trafficlight[2].green_duration /= scaling_factor

            if action[1] == 1:  # Increase right-left green duration
                self.trafficlight[0].green_duration *= scaling_factor
            elif action[1] == 2:  # Decrease right-left green duration
                self.trafficlight[0].green_duration /= scaling_factor

        
            for light in self.trafficlight:
                light.green_duration = max(1000, min(10000, light.green_duration))
                light.red_duration = max(1000, min(10000, light.red_duration)) 
            
            if self.trafficlight[0].colour == "green":
                self.trafficlight[2].red_duration = self.trafficlight[0].green_duration
            elif self.trafficlight[2].colour == "green":
                self.trafficlight[0].red_duration = self.trafficlight[2].green_duration
            
            if len(self.timings) <=4:
                self.timings.append([int(self.trafficlight[2].green_duration),int(self.trafficlight[0].green_duration),int(self.trafficlight[2].green_duration),int(self.trafficlight[0].green_duration)])
            else:
                
                self.timings=[["Traffic1","Traffic2","Traffic3","Traffic4"]]
                
                self.timings.append([int(self.trafficlight[2].green_duration),int(self.trafficlight[0].green_duration),int(self.trafficlight[2].green_duration),int(self.trafficlight[0].green_duration)])
        
        
       
        num = self.f.readline()
        
        if  int(num)== 1:
            self.up_down.make_car()
        if int(num) == 2:
            self.righ_left.make_car()
           
        
        for car in self.righ_left.c:
            car.move(stop_right)
        for car in self.up_down.c:
            car.move(stop_up)

        
        
        congestion = Pu+Pl

        reward -= (congestion) * 2  
        self.negetive_reward = (self.total_cars_stoped) * 2 
        reward += (self.total_cars_passed) * 10
     
        self.frame += 1
        
        done = self.total_cars_passed > 100
    
        self.total_reward = reward
        # self.total_cars_passed = 
        self.total_cars_stoped=congestion
        
       
        
        
        return self.get_obs(), reward, done, {}
        
    def render(self, mode='human'):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode([self.width, self.height])
        
        # Draw the roads
        self.screen.fill("black")
        self.up_down.Intersection(self.screen)
        self.righ_left.Intersection(self.screen)
        
        # Draw the traffic lights
        for light in self.trafficlight:
            light.draw(self.screen)
        
        # Draw the cars
        for car in self.up_down.c:
            car.draw(self.screen)
        for car in self.righ_left.c:
            car.draw(self.screen)
       
        # Draw the green duration timer for each light
        font = pygame.font.Font(None, 30)
        
        traffic_0 = "1"
        t_0 = font.render(traffic_0, True, (255, 255, 255))
        self.screen.blit(t_0, (WIDTH // 2 - road_width // 2 - 70, HEIGHT // 2 + road_width // 2 + 20))
        
        traffic_1 = "2"
        t_1 = font.render(traffic_1, True, (255, 255, 255))
        self.screen.blit(t_1, (WIDTH // 2 - road_width // 2 - 80, 
                                HEIGHT // 2 - road_width // 2 - 55))
        
        traffic_2 = "3"
        t_2 = font.render(traffic_2, True, (255, 255, 255))
        self.screen.blit(t_2, (WIDTH // 2 + road_width // 2 + 40, 
                            HEIGHT // 2 - road_width // 2 - 60))
        
        traffic_3= "4"
        t_3 = font.render(traffic_3, True, (255, 255, 255))
        self.screen.blit(t_3, (WIDTH // 2 + road_width // 2 + 40, 
                                    HEIGHT // 2 + road_width // 2 + 30))
        
        
        if self.trafficlight[2].colour=="green"  and self.trafficlight[0].colour=="red":
            timerG_0 = f"G: {int(self.trafficlight[2].green_duration)} ms"
            textG_0 = font.render(timerG_0, True, (255, 255, 255))
            self.screen.blit(textG_0, (WIDTH // 2 - road_width // 2 - 280, HEIGHT // 2 + road_width // 2 + 20))
            
            timerR_0 = f"R: 0 ms"
            textR_0 = font.render(timerR_0, True, (255, 255, 255))
            self.screen.blit(textR_0, (WIDTH // 2 - road_width // 2 - 280, HEIGHT // 2 + road_width // 2 + 40))
        elif self.trafficlight[2].colour=="red" and self.trafficlight[0].colour=="green" :
            timerG_0 = f"G: 0 ms"
            textG_0 = font.render(timerG_0, True, (255, 255, 255))
            self.screen.blit(textG_0, (WIDTH // 2 - road_width // 2 - 280, HEIGHT // 2 + road_width // 2 + 20))
       
            timerR_0 = f"R: {int(self.trafficlight[2].red_duration)} ms"
            textR_0 = font.render(timerR_0, True, (255, 255, 255))
            self.screen.blit(textR_0, (WIDTH // 2 - road_width // 2 - 280, HEIGHT // 2 + road_width // 2 + 40))
        else:
            timerG_0 = f"G: 0 ms"
            textG_0 = font.render(timerG_0, True, (255, 255, 255))
            self.screen.blit(textG_0, (WIDTH // 2 - road_width // 2 - 280, HEIGHT // 2 + road_width // 2 + 20))
            timerR_0 = f"R: 0 ms"
            textR_0 = font.render(timerR_0, True, (255, 255, 255))
            self.screen.blit(textR_0, (WIDTH // 2 - road_width // 2 - 280, HEIGHT // 2 + road_width // 2 + 40))
         
        
            
        if self.trafficlight[2].colour == "green" and self.trafficlight[0].colour=="red":
        
            timerG_1 = f"G: {int(self.trafficlight[2].green_duration)} ms"
            textG_1 = font.render(timerG_1, True, (255, 255, 255))
            self.screen.blit(textG_1, (WIDTH // 2 + road_width // 2 + 90, 
                            HEIGHT // 2 - road_width // 2 - 80))

            timerR_1 = f"R: 0 ms"
            textR_1 = font.render(timerR_1, True, (255, 255, 255))
            self.screen.blit(textR_1, (WIDTH // 2 + road_width // 2 + 90, 
                            HEIGHT // 2 - road_width // 2 - 60))
    
        elif self.trafficlight[2].colour =="red" and self.trafficlight[0].colour=="green":
            timerG_1 = f"G: 0 ms"
            textG_1 = font.render(timerG_1, True, (255, 255, 255))
            self.screen.blit(textG_1, (WIDTH // 2 + road_width // 2 + 90, 
                            HEIGHT // 2 - road_width // 2 - 80))

            timerR_1 = f"R: {int(self.trafficlight[2].red_duration)} ms"
            textR_1 = font.render(timerR_1, True, (255, 255, 255))
            self.screen.blit(textR_1, (WIDTH // 2 + road_width // 2 + 90, 
                            HEIGHT // 2 - road_width // 2 - 60))
    
        else:
           
            
            timerG_1 = f"G: 0 ms"
            textG_1 = font.render(timerG_1, True, (255, 255, 255))
            self.screen.blit(textG_1, (WIDTH // 2 + road_width // 2 + 90, 
                            HEIGHT // 2 - road_width // 2 - 80))

            timerR_1 = f"R: 0 ms"
            textR_1 = font.render(timerR_1, True, (255, 255, 255))
            self.screen.blit(textR_1, (WIDTH // 2 + road_width // 2 + 90, 
                            HEIGHT // 2 - road_width // 2 - 60))
        
    
    

        if self.trafficlight[0].colour=="green" and self.trafficlight[2].colour=="red":
            
            timerG_2 = f"G: {int(self.trafficlight[0].green_duration)} ms"
            textG_2 = font.render(timerG_2, True, (255, 255, 255))
            self.screen.blit(textG_2, (WIDTH // 2 - road_width // 2 - 280, 
                                HEIGHT // 2 - road_width // 2 - 80))
            
            timerR_2 = f"R: 0 ms"
            textR_2 = font.render(timerR_2, True, (255, 255, 255))
            self.screen.blit(textR_2, (WIDTH // 2 - road_width // 2 - 280, 
                                HEIGHT // 2 - road_width // 2 - 60))
            
            
        
        elif self.trafficlight[0].colour=="red" and self.trafficlight[2].colour=="green":
            
            timerG_2 = f"G: 0 ms"
            textG_2 = font.render(timerG_2, True, (255, 255, 255))
            self.screen.blit(textG_2, (WIDTH // 2 - road_width // 2 - 280, 
                                HEIGHT // 2 - road_width // 2 - 80))
            
            timerR_2 = f"R: {int(self.trafficlight[0].red_duration)} ms"
            textR_2 = font.render(timerR_2, True, (255, 255, 255))
            self.screen.blit(textR_2, (WIDTH // 2 - road_width // 2 - 280, 
                                HEIGHT // 2 - road_width // 2 - 60))
        
        else:
           
            
            timerG_2 = f"G: 0 ms"
            textG_2 = font.render(timerG_2, True, (255, 255, 255))
            self.screen.blit(textG_2, (WIDTH // 2 - road_width // 2 - 280, 
                                HEIGHT // 2 - road_width // 2 - 80))
            
            timerR_2 = f"R: 0 ms"
            textR_2 = font.render(timerR_2, True, (255, 255, 255))
            self.screen.blit(textR_2, (WIDTH // 2 - road_width // 2 - 280, 
                                HEIGHT // 2 - road_width // 2 - 60))
            
            
        if self.trafficlight[0].colour=="green" and self.trafficlight[2].colour=="red":
            timerG_3 = f"G: {int(self.trafficlight[0].green_duration)} ms"
            textG_3 = font.render(timerG_3, True, (255, 255, 255))
            self.screen.blit(textG_3, (WIDTH // 2 + road_width // 2 + 90, 
                                    HEIGHT // 2 + road_width // 2 + 20))
                
            timerR_3 = f"R: 0 ms"
            textR_3 = font.render(timerR_3, True, (255, 255, 255))
            self.screen.blit(textR_3, (WIDTH // 2 + road_width // 2 + 90, 
                                    HEIGHT // 2 + road_width // 2 + 40))
            
            
        elif self.trafficlight[0].colour=="red" and self.trafficlight[2].colour=="green":
            timerG_3 = f"G: 0 ms"
            textG_3 = font.render(timerG_3, True, (255, 255, 255))
            self.screen.blit(textG_3, (WIDTH // 2 + road_width // 2 + 90, 
                                    HEIGHT // 2 + road_width // 2 + 20))
                
            timerR_3 = f"R: {int(self.trafficlight[0].red_duration)} ms"
            textR_3 = font.render(timerR_3, True, (255, 255, 255))
            self.screen.blit(textR_3, (WIDTH // 2 + road_width // 2 + 90, 
                                    HEIGHT // 2 + road_width // 2 + 40))  
        else:
            
            
            timerG_3 = f"G: 0 ms"
            textG_3 = font.render(timerG_3, True, (255, 255, 255))
            self.screen.blit(textG_3, (WIDTH // 2 + road_width // 2 + 90, 
                                    HEIGHT // 2 + road_width // 2 + 20))
                
            timerR_3 = f"R: 0 ms"
            textR_3 = font.render(timerR_3, True, (255, 255, 255))
            self.screen.blit(textR_3, (WIDTH // 2 + road_width // 2 + 90, 
                                    HEIGHT // 2 + road_width // 2 + 40))  
            
        
        if self.bufferL<1000:
            timer_t = f"BUFFER ON: {self.bufferL} ms"
            timer_surface = font.render(timer_t, True, (250, 250, 250))
            self.screen.blit(timer_surface, (10, 50))
        elif self.bufferU<1000:
            timer_t = f"BUFFER ON: {self.bufferU} ms"
            timer_surface = font.render(timer_t, True, (250, 250, 250))
            self.screen.blit(timer_surface, (10, 50))
            
        timer_t = f"timer: {self.trafficlight[0].t} ms"
        timer_surface = font.render(timer_t, True, (250, 250, 250))
        self.screen.blit(timer_surface, (10, 20))
        
        reward_text = f"total_reward: {self.total_reward}"
        reward_ = font.render(reward_text, True, (250, 250, 250))
        self.screen.blit(reward_, (10, 80))
        
        cars_passed_text = f"total cars passed: {self.total_cars_passed}"
        cars_passed_ = font.render(cars_passed_text, True, (250, 250, 250))
        self.screen.blit(cars_passed_, (10, 100))
        
        cars_stopped_text = f"total cars stoped: {self.total_cars_stoped}"
        cars_stopped_ = font.render(cars_stopped_text, True, (250, 250, 250))
        self.screen.blit(cars_stopped_, (10, 120))
        
        
        
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (200, 200, 200)

        # Font
        FONT = pygame.font.Font(None, 20)
        for row_idx, row in enumerate(self.timings):
            for col_idx, cell in enumerate(row):
                # Calculate the cell position
                x = 600+col_idx * CELL_WIDTH
                y = 30+row_idx * CELL_HEIGHT

                # Draw the cell rectangle
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_WIDTH, CELL_HEIGHT), 1)

                # Render the text for the cell
                text_surface = FONT.render(str(cell), True, WHITE)
                text_rect = text_surface.get_rect(center=(x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2))
                self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None
    


# env = TrafficLighAi()

# model = PPO("MlpPolicy", env, verbose=2)
# model.learn(total_timesteps=100000)
# model.save("ppo_traffic_model")


# Debug: Monitor environment


