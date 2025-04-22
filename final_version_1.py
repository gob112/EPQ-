import gym
from gym import spaces
import numpy as np
import pygame
import random
from final_version_0 import Road_direction
from stable_baselines3 import PPO


# defining constant (position of the stop lines)
stop_line_bottom = 1000//2 + 90//2 + 20
stop_line_top = 1000//2 - 23 - 90//2
stop_line_right = 1000//2 - 90//2 - 20
stop_line_left = 1000//2 + 90//2 + 20

class TrafficLighAi(gym.Env):
    #Displays the environment visually in a way humans can observe
    metadata = {"render.mode":["human"]}
    def __init__(self):
        super(TrafficLighAi,self).__init__()
        # how many actions my agent can take ( 3 actions - increase red light, decrease green light, do nothing)
        self.action_space = spaces.MultiDiscrete([3, 3])
        # defines the shape of the array holding in information about my enviroment
        self.observation_space=spaces.Box(low=0,high=100,shape=(8,),dtype=np.float32)
        
        self.width = 1000
        self.height = 1000
        self.car_speed = 0.1
        self.road_width = 90
        self.bufferU = 1000
        self.bufferL = 1000
        self.righ_left = Road_direction("right_left")
        self.up_down = Road_direction("up_down")
        # intialieses/make all traffic lights and store it as an attribute for easier manipulation of its properties
        self.trafficlight = self.initialize_trafficlight() 
        self.screen = None
        self.running = False
    #makes traffic ligts and store them in a list
    def initialize_trafficlight(self):
        left_light,righ_light = self.righ_left.make_traffic_light()
        up_light,down_light = self.up_down.make_traffic_light()
        return [left_light,righ_light,up_light,down_light]
    
    # starting point of all episodes
    def reset(self):
        self.frame = 0
        self.up_down.c = []
        self.righ_left.c = []
        for light in self.trafficlight:
            if light.direc =="l" or light.direc == "r":
                light.colour = "red"
                light.green_duration = 3000
                light.red_duration = 3000
            elif light.direc =="u" or light.direc == "d":
                light.colour = "green"
                light.green_duration = 3000
                light.red_duration = 3000
        return self.get_obs()
    # gets all information about enviroment
    def get_obs(self):
        cu = 0
        cr = 0
        cl = 0
        cd = 0
        tr = []
        #number of cars on each road
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
        # state of the traffic lights
        for t in self.trafficlight:
            if t.colour =="red":
                tr.append(1)
            elif t.colour == "green":
                tr.append(0)
                
        return np.array([cu,cd,cl,cr]+tr,dtype = np.float32)
    
    def step(self,action):
        u = 0
        d = 0
        l = 0
        r = 0 
        ch = False
        reward = 0
        done = False
        # number of cars before the stop line
        for car in self.up_down.c:
            if car.direction == "u" and car.y > stop_line_bottom:
                u+=1
                
            elif car.direction == "d" and car.y < stop_line_top:
                d +=1
        for car in self.righ_left.c:
            if car.direction == "r" and car.x > stop_line_left:
                r+=1
            elif car.direction == "l" and car.x < stop_line_right:
                l +=1
        #only update the traffic timers when buffer timer is not decreasing
        if self.bufferU>=1000 and self.bufferL >=1000:
            self.trafficlight[0].update_timer()
            self.trafficlight[2].update_timer()
        # if traffic light duration is expired, check if its turing from red to green if so start a buffer, 
        # ones buffer changes, change the traffic light
        #if turning from green to red change without buffer
        # logic for left and right road
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
                ch =True
        # light changing logic for up and downn road
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
                ch =True
        # only if a light is changing colours 
        if ch:
            # change the green duration based on the action the agent takes
            scaling_factor = 1.1
            if action[0] == 1:  # Increase up-down green duration
                self.trafficlight[2].green_duration *= scaling_factor
            elif action[0] == 2:  # Decrease up-down green duration
                self.trafficlight[2].green_duration /= scaling_factor
            if action[1] == 1:  # Increase right-left green duration
                self.trafficlight[0].green_duration *= scaling_factor
            elif action[1] == 2:  # Decrease right-left green duration
                self.trafficlight[0].green_duration /= scaling_factor
            # makes sure the duration does not pass the limits
            for light in self.trafficlight:
                light.green_duration = max(1000, min(10000, light.green_duration))
                light.red_duration = max(1000, min(10000, light.red_duration)) 
            # if the up down road is green the duration of the red light for the left and right should be the same as green duration of up and down
            if self.trafficlight[0].colour == "green":
                self.trafficlight[2].red_duration = self.trafficlight[0].green_duration
             # if the left right road is green the duration of the red light for the up down should be the same as green duration of left right
            elif self.trafficlight[2].colour == "green":
                self.trafficlight[0].red_duration = self.trafficlight[2].green_duration
        
        #stores a boolean value if a car coming from a certain direction should stop or not, based on the colour of the light
        stop_up = self.trafficlight[2].stop_or_not()
        stop_right = self.trafficlight[1].stop_or_not()
        
        #makes a car randomly
        if random.randint(1,50) == 1:
            self.up_down.make_car()
           
        if random.randint(1,50) == 2:
            self.righ_left.make_car()
        
        #moves the car
        for car in self.righ_left.c:
            car.move(stop_right)
        for car in self.up_down.c:
            car.move(stop_up)

        cars_passed = sum(1 for car in self.up_down.c if car.y < stop_line_top) + \
                    sum(1 for car in self.righ_left.c if car.x > stop_line_right)
        # reward calculation
        congestion = (u+d+l+r)
        reward += cars_passed * 10  
        reward -= congestion * 5  
        self.frame += 1
        # condiotion for a completion of an episode
        done = congestion > 1000
    
        return self.get_obs(), reward, done, {}
    # function to display the simulation/ render the window 
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
            
        pygame.display.flip()
        
    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None
    
env = TrafficLighAi()
# trains the agent
model = PPO("MlpPolicy", env, verbose=2)
model.learn(total_timesteps=1000)

# Debug: Monitor environment
obs = env.reset()
# tests and shows how the agent is using the new model in making decisions.
for _ in range(100000):  
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()