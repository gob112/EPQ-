import pygame
import random 
pygame.init()
import csv



WIDTH = 1000
HIEGHT = 1000

CAR_SIZE = (30,30)
CAR_SPEED = 0.7

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
            pygame.draw.line(screen, "red", ((WIDTH)//2 + 23 - stop_line_length//2, (WIDTH)//2 - (road_width)//2 - 20), 
                        (WIDTH//2 +23 + stop_line_length//2, WIDTH//2 - road_width//2 - 20), line_thickness)
            #bottom
            pygame.draw.line(screen, "white", (WIDTH//2 - 23 - stop_line_length//2, WIDTH//2 + road_width//2 + 20), 
                        (WIDTH//2 - 23 + stop_line_length//2, WIDTH//2 + road_width//2 + 20), line_thickness)
       
        elif self.road == "right_left":
            #left
            pygame.draw.rect(screen,"grey",(0, WIDTH//2 - road_width//2, HIEGHT, road_width))
            pygame.draw.line(screen,"white",(0,HIEGHT//2),(WIDTH,HIEGHT//2),5)
            # top
            pygame.draw.line(screen,"red", (WIDTH//2 - road_width//2 - 20,HIEGHT//2 - 23 - stop_line_length//2),
                        (WIDTH//2-road_width//2 - 20 ,HIEGHT//2 - 23 + stop_line_length//2),line_thickness)
        
            #right
            pygame.draw.line(screen,"red", (WIDTH//2 + road_width//2 + 20,HIEGHT//2 + 23 - stop_line_length//2),
                     (WIDTH//2+road_width//2 + 20 ,HIEGHT//2 + 23 + stop_line_length//2),line_thickness)
        
    class Traffic_light:
        def __init__(self,x,y,red_due,green_due,defualt,direction):
            self.xt = x
            self.yt = y
            self.colour = defualt
            self.t = 0
            self.green_duration = green_due
            self.red_duration = red_due
            self.direc = direction
            self.buffer = False
            self.buffer_timer = 0
            
            
        def change(self):
            if self.colour == "green":
                self.colour="red"
                self.buffer=True
                #self.u_buffer()
               
            elif self.colour == "red" :
                #self.buffer = False
                #self.buffer_timer = 0
                self.colour="green"
           
            self.reset_timer()
            
        def stop_or_not(self):
            if self.colour == "red":
                return True
            else:
                return False
        def should_change(self):
            #print("hallo",self.colour,self.green_duration,self.red_duration,self.t)
          
            if self.colour == "green" and self.t >= self.green_duration:
                return True
            elif self.colour == "red" and self.t >= self.red_duration :
                return True
            return False
        def update_timer(self):
            self.t+=1
        def u_buffer(self):
            self.buffer_timer+=1
        def reset_timer(self):
            self.t=0
        def draw(self,screen):
            pygame.draw.rect(screen,"grey",(self.xt,self.yt,25,25))
            pygame.draw.circle(screen,self.colour,(self.xt +12,self.yt+12),10)
            
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
            lightUp = self.Traffic_light(WIDTH//2 +50, HIEGHT // 2 -80 ,3000,3000,"red","u") # up
            lightDown = self.Traffic_light(WIDTH//2 -80, HIEGHT // 2 +50,3000,3000,"red","d")# down
            return [lightUp,lightDown]
        elif self.road == "right_left":
            lightRight = self.Traffic_light(WIDTH//2 +50, HIEGHT // 2 +50 ,3000,3000,"green","l") # left
            lightLeft = self.Traffic_light(WIDTH//2 -80, HIEGHT // 2 -80 ,3000,3000,"green","r") # right
            return [lightRight,lightLeft]





class Run():
    def __init__(self):
        self.frame = 0
        self.total_cars_passed_up_down = 0
        self.total_cars_passed_right_left = 0
        self.congestion_up_down = 0
        self.congestion_right_left = 0  
    def reset(self):
        self.total_cars_passed_up_down = 0
        self.total_cars_passed_right_left = 0
        self.congestion_up_down = 0
        self.congestion_right_left = 0
    def run(self):
       
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
        
        
       
        
        
        f.close()
        while running:
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    f.close()
                    running = False

            # Fill the background with white
            
            # if self.frame==5600000:
            #     running=False
          
                
                
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
            
            
            self.frame += 1
            
            f = open("random_number.txt","r")
            nums = f.readlines()
            
            if self.frame == len(nums):
                self.frame==0
            else:
                num = nums[self.frame]
          
            #print("num",num)
           
            if not stopU:
                if int(num) == 1:
                    UP_road.make_car()
                    
      
            if not stopL:
                if int(num) == 2:
                    LEFT_road.make_car()
                
            
            for v in UP_road.c:
                if not v.lines_passed:
                # Check the conditions for cars moving up or down
                    if v.direction == "u" and v.y <= WIDTH // 2 + 85:  # Car moving up has passed the stop line
                        v.lines_passed = True
                        self.total_cars_passed_up_down += 1  # Increment the counter for up-down road
                        
                    elif v.direction == "d" and v.y >= WIDTH // 2 - 100:  # Car moving down has passed the stop line
                        v.lines_passed = True
                        self.total_cars_passed_up_down += 1
                v.move(stopU)
                v.draw(screen)
            
                
            for v in LEFT_road.c:
                if not v.lines_passed:
                # Check the conditions for cars moving left or right
                    if v.direction == "l" and v.x <= WIDTH // 2 + 100:  # Car moving left has passed the stop line
                        v.lines_passed = True
                        self.total_cars_passed_right_left += 1  # Increment the counter for left-right road
                        
                    elif v.direction == "r" and v.x >= WIDTH // 2 - 100:  # Car moving right has passed the stop line
                        v.lines_passed = True
                        self.total_cars_passed_right_left += 1 
                v.move(stopL)
                v.draw(screen)
       
            
                
                
            lightU.draw(screen)
            lightD.draw(screen)
            lightL.draw(screen)
            lightR.draw(screen)
            self.congestion_up_down = sum(
                1 for v in UP_road.c if not v.lines_passed and ((v.direction == "u" and v.y >= WIDTH // 2 + 85 and stopU) or
                                                                (v.direction == "d" and v.y <= WIDTH // 2 - 100 and stopU))
            )

            self.congestion_right_left = sum(
                1 for v in LEFT_road.c if not v.lines_passed and ((v.direction == "l" and v.x >= WIDTH // 2 + 100 and stopL) or
                                                                (v.direction == "r" and v.x <= WIDTH // 2 - 100 and stopL))
            )

            total_congestion = self.congestion_up_down + self.congestion_right_left
            font = pygame.font.SysFont(None, 36)  # Set font size
            congestion_text = font.render(f"Congestion: {total_congestion} cars stopped", True, "white")
            screen.blit(congestion_text, (10, 10)) 
            
            total_passed = self.total_cars_passed_up_down + self.total_cars_passed_right_left
            passed_text = font.render(f"Cars Passed: {total_passed}", True, "white")
            screen.blit(passed_text, (10, 40))
            if total_passed ==100:
                with open("No_RL.csv","a",newline="") as f:
                    x = csv.writer(f)
                    x.writerow([total_congestion,])
                self.total_cars_passed_up_down =0
                self.total_cars_passed_right_left=0
                self.reset()
            # Flip the display
            pygame.display.flip()
            f.close
        # Done! Time to quit.
        pygame.quit()

        