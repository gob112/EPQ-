import pygame
import random 
pygame.init()

WIDTH = 1000
HIEGHT = 1000

CAR_SIZE = (30,30)
CAR_SPEED = 1

#defining costant variables
START_TOP = (HIEGHT//2+5,0) # top stop line
START_RIGHT = (0,WIDTH//2-35) # right stop line
START_LEFT = (WIDTH-5,WIDTH//2 +5) # left stop line
START_BOTTOM = (WIDTH//2-35,HIEGHT-150) # bottom stop line
road_width = 90
stop_line_length = 45  # Length of the stop lines
line_thickness = 5
start_up_down = [START_BOTTOM,START_TOP]
start_right_left = [START_RIGHT,START_LEFT]
color = ["pink","purple","blue","orange"]


class Road_direction:
    
    def __init__(self,road_dire):
        self.road = road_dire
        self.c = []
        
    #drawing the road and the stop lines
    def Intersection(self,screen):
        # up_down road
        if self.road == "up_down":
            pygame.draw.rect(screen,"grey",( WIDTH//2 - road_width//2,0, road_width,WIDTH))
            pygame.draw.line(screen,"white",(HIEGHT//2,0),(HIEGHT//2,WIDTH),5)
            pygame.draw.line(screen, "white", ((WIDTH)//2 + 23 - stop_line_length//2, (WIDTH)//2 - (road_width)//2 - 20), 
                        (WIDTH//2 +23 + stop_line_length//2, WIDTH//2 - road_width//2 - 20), line_thickness)
            #bottom
            pygame.draw.line(screen, "white", (WIDTH//2 - 23 - stop_line_length//2, WIDTH//2 + road_width//2 + 20), 
                        (WIDTH//2 - 23 + stop_line_length//2, WIDTH//2 + road_width//2 + 20), line_thickness)
       
       #right left road
        elif self.road == "right_left":
            #left
            pygame.draw.rect(screen,"grey",(0, WIDTH//2 - road_width//2, HIEGHT, road_width))
            pygame.draw.line(screen,"white",(0,HIEGHT//2),(WIDTH,HIEGHT//2),5)
            # top
            pygame.draw.line(screen,"white", (WIDTH//2 - road_width//2 - 20,HIEGHT//2 - 23 - stop_line_length//2),
                        (WIDTH//2-road_width//2 - 20 ,HIEGHT//2 - 23 + stop_line_length//2),line_thickness)
        
            #right
            pygame.draw.line(screen,"white", (WIDTH//2 + road_width//2 + 20,HIEGHT//2 + 23 - stop_line_length//2),
                     (WIDTH//2+road_width//2 + 20 ,HIEGHT//2 + 23 + stop_line_length//2),line_thickness)
            
    #defining traffic lights properties and actions it can take
    class Traffic_light:
        def __init__(self,x,y,red_due,green_due,defualt,direction):
            self.xt = x
            self.yt = y
            self.colour = defualt
            self.t = 0
            self.green_duration = green_due
            self.red_duration = red_due
            self.direc = direction
           
        # changing light from red to green or green to red
        def change(self):
            if self.colour == "green":
                self.colour="red"
            elif self.colour == "red" :
                self.colour="green"
            self.reset_timer()
            
        #returns if a car should stop or not based on the color of the light
        def stop_or_not(self):
            if self.colour == "red":
                return True
            else:
                return False
            
        #checks if a light should change colour (if its red or green duration has expired)
        def should_change(self):
            if self.colour == "green" and self.t >= self.green_duration:
                return True
            elif self.colour == "red" and self.t >= self.red_duration :
                return True
            return False
        
        def update_timer(self):
            self.t+=1
           
        def reset_timer(self):
            self.t=0
            
        #draws the traffic light
        def draw(self,screen):
            pygame.draw.rect(screen,"grey",(self.xt,self.yt,25,25))
            pygame.draw.circle(screen,self.colour,(self.xt +12,self.yt+12),10)
    #defines cars there properties and the actions they can take.
    class Vehical:
        def __init__(self,x,y,width,hieght,speed, colour,direction,road,c):
            self.x = float(x)
            self.y = float(y)
            self.r = pygame.Rect(int(self.x),int(self.y),width,hieght)
            self.colour = colour
            self.speed = speed
            self.direction = direction
            self.road = road
            self.lines_passed = False
            self.c = c
            
        #moves the car
        def move(self,stoped):
            # moves car in the up  down road
            if self.road == "up_down":
                #logic to move the up cars (cars going from bottom to top)
                if self.direction == "u":
                    # stops the car if red light and before the stop line
                    if not self.lines_passed and int(self.y) >=(WIDTH//2 +85) and stoped:  
                        return 
                    elif (self.y) <= (WIDTH//2 + 85):
                        self.lines_passed = True
                    # moves the car if not green light or passed the stop line
                    self.y -= self.speed
                
                #moves car in down road (cars going from top to bottom of the screen)
                if self.direction == "d":
                    if not self.lines_passed and int(self.y) <= (WIDTH//2 - 100) and stoped:
                        return
                    elif (self.y) >= (WIDTH//2 - 100):
                        self.lines_passed = True
                    self.y += self.speed
                self.r.topleft = (int(self.x),int(self.y))
                         
            #moves car in the left right road
            elif self.road == "right_left":
                
                if self.direction == "l":
                    if not self.lines_passed and (self.x) >= (WIDTH//2 +100) and stoped:
                        return 
                    elif (self.x)<= (WIDTH//2+100 ):
                        self.lines_passed = True
                    self.x -= self.speed
                   
                    
                    
                elif self.direction == "r":
                    if not self.lines_passed and (self.x) <=(WIDTH//2  -100 ) and stoped:
                        return 
                    elif (self.x)>= (WIDTH//2 -100):
                        self.lines_passed=True
                    self.x +=self.speed
                self.r.topleft = (int(self.x),int(self.y))
        # draws the car
        def draw(self,screen):
            pygame.draw.rect(screen,self.colour,self.r)
    # function to make a car by defining where it should start, on which road and what colour
    def make_car(self):
        r_color = random.choice(color)
        # makes car in up down road
        if self.road == "up_down":
            r_start = random.choice(start_up_down)
            if r_start == START_BOTTOM:
                
                v = self.Vehical(*START_BOTTOM,*CAR_SIZE,CAR_SPEED,r_color,"u",self.road,self.c)
                # if any cars in the list of cars do not collide then create the car and add it to the list of cars
                if all(not v.r.colliderect(x.r) for x in self.c):
                    self.c.append(v)
            elif r_start == START_TOP:
                v = self.Vehical(*START_TOP,*CAR_SIZE,CAR_SPEED,r_color,"d",self.road,self.c)
                if all(not v.r.colliderect(x.r) for x in self.c):
                    self.c.append(v)
                    
        #makes car in left right road
        if self.road == "right_left":
            
            r_start = random.choice(start_right_left)
            if r_start == START_LEFT:
                v = self.Vehical(*START_LEFT,*CAR_SIZE,CAR_SPEED,r_color,"l",self.road,self.c)
                if all(not v.r.colliderect(x.r) for x in self.c):
                    self.c.append(v)
            elif r_start == START_RIGHT:
                v = self.Vehical(*START_RIGHT,*CAR_SIZE,CAR_SPEED,r_color,"r",self.road,self.c)
                if all(not v.r.colliderect(x.r) for x in self.c):
                    self.c.append(v)
                   
    
    def make_traffic_light(self):
        if self.road == "up_down":
            lightUp = self.Traffic_light(WIDTH//2 +50, HIEGHT // 2 -80 ,3000,3000,"red","u") # up
            lightDown = self.Traffic_light(WIDTH//2 -80, HIEGHT // 2 +50,3000,3000,"red","d")# down
            return [lightUp,lightDown]
        elif self.road == "right_left":
            lightRight = self.Traffic_light(WIDTH//2 +50, HIEGHT // 2 +50 ,3000,3000,"green","l") # left
            lightLeft = self.Traffic_light(WIDTH//2 -80, HIEGHT // 2 -80 ,3000,3000,"green","r") # right
            return [lightRight,lightLeft]



    

        
        
        


