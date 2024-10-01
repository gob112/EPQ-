import pygame
import random 
pygame.init()

WIDTH = 1000
HIEGHT = 1000

CAR_SIZE = (30,30)
CAR_SPEED = 0.1

START_TOP = (HIEGHT//2+5,0)
START_RIGHT = (0,WIDTH//2-35)
START_LEFT = (WIDTH-5,WIDTH//2 +5)
START_BOTTOM = (WIDTH//2-35,HIEGHT-150)
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
    
    def Intersection(self,screen):
      
        if self.road == "up_down":
            pygame.draw.rect(screen,"grey",( WIDTH//2 - road_width//2,0, road_width,WIDTH))
            pygame.draw.line(screen,"white",(HIEGHT//2,0),(HIEGHT//2,WIDTH),5)
            pygame.draw.line(screen, "white", ((WIDTH)//2 + 23 - stop_line_length//2, (WIDTH)//2 - (road_width)//2 - 20), 
                        (WIDTH//2 +23 + stop_line_length//2, WIDTH//2 - road_width//2 - 20), line_thickness)
            #bottom
            pygame.draw.line(screen, "white", (WIDTH//2 - 23 - stop_line_length//2, WIDTH//2 + road_width//2 + 20), 
                        (WIDTH//2 - 23 + stop_line_length//2, WIDTH//2 + road_width//2 + 20), line_thickness)
       
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
        
    class Traffic_light:
        def __init__(self,x,y,red_due,green_due,defualt,start_time,direction):
            self.x = x
            self.y = y
            self.colour = defualt
            self.timer = start_time
            self.t = start_time
            self.green_duration = red_due
            self.red_duration = green_due
            self.direc = direction
        def change(self):
            if self.colour == "green":
                self.colour="red"
            elif self.colour == "red":
                self.colour="green"
            
        def stop_or_not(self):
            if self.colour == "red":
                return True
            else:
                return False
        def direction(self):
            return self.direc
        def draw(self,screen):
            pygame.draw.rect(screen,"grey",(self.x,self.y,25,25))
            pygame.draw.circle(screen,self.colour,(self.x +12,self.y+12),10)
            
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

        def move(self,stoped):
            if self.road == "up_down":
                if self.direction == "u":
                    if not self.lines_passed and int(self.y) >=(WIDTH//2 +85) and stoped:  
                        return 
                    elif (self.y) <= (WIDTH//2 + 85):
                        self.lines_passed = True
                    
                    self.y -= self.speed
                
                if self.direction == "d":
                    if not self.lines_passed and int(self.y) <= (WIDTH//2 - 100) and stoped:
                        return
                    elif (self.y) >= (WIDTH//2 - 100):
                        self.lines_passed = True
                    self.y += self.speed
                self.r.topleft = (int(self.x),int(self.y))
                         
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
            
        def draw(self,screen):
            pygame.draw.rect(screen,self.colour,self.r)

    def make_car(self):
        r_color = random.choice(color)
        if self.road == "up_down":
            r_start = random.choice(start_up_down)
            if r_start == START_BOTTOM:
                
                v = self.Vehical(*START_BOTTOM,*CAR_SIZE,CAR_SPEED,r_color,"u",self.road,self.c)
                
                if all(not v.r.colliderect(x.r) for x in self.c):
                    self.c.append(v)
                    
            elif r_start == START_TOP:
               
                v = self.Vehical(*START_TOP,*CAR_SIZE,CAR_SPEED,r_color,"d",self.road,self.c)
                if all(not v.r.colliderect(x.r) for x in self.c):
                    self.c.append(v)
                       
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
            lightUp = self.Traffic_light(WIDTH//2 +50, HIEGHT // 2 -80 ,3000,3000,"red",0,"u") # up
            lightDown = self.Traffic_light(WIDTH//2 -80, HIEGHT // 2 +50,3000,3000,'red',0,"d")# down
            return [lightUp,lightDown]
        elif self.road == "right_left":
            lightRight = self.Traffic_light(WIDTH//2 +50, HIEGHT // 2 +50 ,3000,3000,"green",0,"l") # left
            lightLeft = self.Traffic_light(WIDTH//2 -80, HIEGHT // 2 -80 ,3000,3000,"green",0,"r") # right
            return [lightRight,lightLeft]


frame = 0
screen = pygame.display.set_mode([WIDTH,HIEGHT])
running = True

UP_road = Road_direction("up_down")
LEFT_road = Road_direction("right_left")

lightU,lightD = UP_road.make_traffic_light()

lightR,lightL = LEFT_road.make_traffic_light()

t=0
flag = True
light_timer=3000
leflightcolor= lightL.colour
uplightcolour = lightU.colour
continue_timer = 1
initial_flag = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill("black")

    
    stopU = lightU.stop_or_not()
    stopL = lightL.stop_or_not()
    
    t +=1
    
    if t == light_timer and flag == True and lightL.colour == leflightcolor and continue_timer <=2: 
        lightL.change()
        lightR.change()
        leflightcolor = lightL.colour
        
        if initial_flag == True:
            continue_timer +=1
            initial_flag = False
            
        if continue_timer ==2:
            flag = False
            continue_timer +=1
            light_timer +=1000
        else:
            light_timer +=3000
            continue_timer +=1
        
        
        
    if t == light_timer and flag == False and lightU.colour == uplightcolour and (continue_timer <=4 and continue_timer > 2):
       
        lightD.change()
        lightU.change()
        uplightcolour = lightU.colour
        if continue_timer ==4:
            flag = True
            continue_timer = 1
            light_timer +=1000
        else:
            light_timer +=3000
            continue_timer += 1
        
        
    UP_road.Intersection(screen)
    LEFT_road.Intersection(screen)
    
    stopU = lightU.stop_or_not()
    stopL = lightL.stop_or_not()
    
    
    frame += 1
    
    if not stopU:
        if random.randint(1,100) == 10:
            UP_road.make_car()
        
    if not stopL:
        if random.randint(1,100) == 2:
            LEFT_road.make_car()
           
    
    for v in UP_road.c:
        v.move(stopU)
        v.draw(screen)
        
    for v in LEFT_road.c:
       
        v.move(stopL)
        v.draw(screen)
   
                
    lightU.draw(screen)
    lightD.draw(screen)
    lightL.draw(screen)
    lightR.draw(screen)
    
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()