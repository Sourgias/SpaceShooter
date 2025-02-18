# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:43:24 2025

@author: User
"""


import pygame
import random 
import math

class Blue(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image= pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\PlanetBlue.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 5, self.image.get_height() * 5))
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, 0))
        
    def update(self):
        self.rect.move_ip(0, 1)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\tiny_ship17.png").convert_alpha()             
        self.image = pygame.transform.scale_by(self.image, 3)             
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.Vector2()        
        self.speed = 9
        self.can_shoot = True  # Flag to control shooting
        self.laser_shoot_time = 0
        self.cooldown_duration = 500  # 500 ms cooldown (half a second)
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Update movement direction based on input
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed

        # Call the laser timer to handle shooting cooldown
        self.laser_timer()

        # Handle shooting
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.fire_laser()
            self.can_shoot = False  # Prevent firing until the cooldown is over
            self.laser_shoot_time = pygame.time.get_ticks()
            
    def fire_laser(self):
        Laser(all_sprites, self)  # Pass the player instance to the laser

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)

        self.image = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\lasser02.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image,90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx 
        self.rect.bottom = player.rect.bottom      
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.y -= 20  #Laser -speed

        #Collision with Comet1
        for comet in all_sprites:
            if isinstance(comet, Comet1):  
                if pygame.sprite.collide_mask(self, comet):  
                    comet.kill()  
                    self.kill()  
                    print("Laser hit Comet1 and destroyed it!")
                    break  
        
        #Collision with Comet 2
        for comet in all_sprites:
            if isinstance(comet, Comet2):
                if pygame.sprite.collide_mask(self,comet):
                    comet.kill()
                    self.kill()
                    print("Comet1 Splitted")
                     
                    Comet1(groups=all_sprites, x=comet.rect.centerx, y=comet.rect.centery, angle=random.randint(65, 85))
                    
                    Comet1(groups=all_sprites, x=comet.rect.centerx, y=comet.rect.centery, angle=random.randint(90, 140))
                    break


        if self.rect.bottom < 0:
            self.kill()

                
#Comet 1
class Comet1(pygame.sprite.Sprite):
    def __init__(self, groups, x=None, y=None, angle=None):
        super().__init__(groups)

        self.image = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\comet_1.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 2)
        self.image =pygame.transform.rotate(self.image, random.randint(0, 360))
        self.rect = self.image.get_rect()

        if x is None or y is None:
            self.rect.center = (random.randint(0, WINDOW_WIDTH), 0)
        else:
            self.rect.center = (x, y)

        # Apply random rotation to the comet
        rotation_angle = random.randint(0, 360)  # Random rotation from 0 to 360 degrees
        self.image = pygame.transform.rotate(self.image, rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Reposition the rect after rotation
        
        self.mask = pygame.mask.from_surface(self.image)

        # If no angle is passed, set it to a random downward direction
        self.angle = angle if angle is not None else random.randint(75,120)
        current_time=pygame.time.get_ticks() 
        self.speed = 7   # Set a fixed speed for the comet

    def update(self):
        # Convert the angle to radians
        radian_angle = math.radians(self.angle)

        # Calculate the movement in the x and y directions based on the angle
        dx = self.speed * math.cos(radian_angle)
        dy = self.speed * math.sin(radian_angle)

        # Update the position of the comet
        self.rect.move_ip(dx, dy)

        # Remove the comet if it goes off-screen
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


#Comet 2
class Comet2(pygame.sprite.Sprite):
    def __init__(self, groups, x=None, y=None, angle=None):
        super().__init__(groups)
        #print("Comet created!")  # Debug print
    
        self.image = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\comet_2.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 2)
        self.image =pygame.transform.rotate(self.image, random.randint(0, 360))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WINDOW_WIDTH), 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle if angle is not None else random.randint(75,120)
        
        self.rotation_speed = random.randint(2,5) 
    def update(self):
        #print(f"Comet position: {self.rect.center}")  # Debug print
        radian_angle =math.radians(self.angle)
        self.speed = 4
        dx = self.speed * math.cos(radian_angle)
        dy = self.speed * math.sin(radian_angle)

        self.rect.move_ip(dx, dy)
        if self.rect.top > WINDOW_HEIGHT:
           # print("Comet removed!")  # Debug print
            self.kill()


def display_score():
    current_time = pygame.time.get_ticks() // 1000  # Convert milliseconds to seconds
    text_surf = font.render(str(current_time), True, 'white')
    
    # Create a rectangle for positioning
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    
    # Blit the text to the display surface
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, "white" , text_rect.inflate(20, 17).move(0,-3),7,7)

pygame.init()

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 1000

display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

clock= pygame.time.Clock()

font =pygame.font.Font(r"C:\Users\User\Desktop\Space Shotoer\SRAFreePixelFontPack\PixelMiddle.ttf",40)
text_surf = font.render("test",True,'white')

#import images
#Ship/lasser
# ship = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\tiny_ship17.png").convert_alpha()
# ship2 = pygame.transform.scale_by(ship,1)
# ship2_rect = ship2.get_rect(center= (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

all_sprites = pygame.sprite.Group()
blue = Blue(groups= all_sprites)
comet1 = Comet1(groups=all_sprites)
comet2 = Comet2(groups=all_sprites)
player= Player(all_sprites)


laser = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\lasser02.png").convert_alpha()
laser2 = pygame.transform.scale_by(laser,2)
laser_rect = laser2.get_rect(bottomleft=(20,WINDOW_HEIGHT-20))

#comet/plannets
comet_1 = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\comet_1.png").convert_alpha()
comet_1_2 = pygame.transform.scale_by(comet_1,3)
comet_1_rect = comet_1_2.get_rect(center = (WINDOW_WIDTH/3, WINDOW_HEIGHT/3))

comet_2 = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\comet_2.png").convert_alpha()
comet_2_2 = pygame.transform.scale_by(comet_2,3)
comet_2_rect= comet_2_2.get_rect(center=(WINDOW_WIDTH/4,WINDOW_HEIGHT/4))

PlanetBlue = pygame.image.load(r"C:\Users\User\Desktop\Space Shotoer\PlanetBlue.png").convert_alpha()
PlanetBlue2 = pygame.transform.scale_by(PlanetBlue, 10)


# Load star image
star_image_path = r"C:\Users\User\Desktop\Space Shotoer\stars.png"  
original_star = pygame.image.load(star_image_path).convert_alpha()

# Function to generate random star transformations
def gen_random_star(image):
    # Random scaling
    scale_factor = random.uniform(0.5, 2)
    scaled_star = pygame.transform.scale_by(image, scale_factor)
    
    # Random rotation
    angle = random.randint(0, 360)
    rotated_star = pygame.transform.rotate(scaled_star, angle)
    
    return rotated_star

# Generate 5 random stars with positions
stars = []
for _ in range(15):
    transformed_star = gen_random_star(original_star)
    x = random.randint(0, WINDOW_WIDTH - transformed_star.get_width())
    y = random.randint(0, WINDOW_HEIGHT - transformed_star.get_height())
    stars.append((transformed_star, (x, y)))




# VARIABLES
# player_speed = 9
# player_direction = pygame.math.Vector2(-0,0)
# can_shoot = True

SPAWN_COMET_EVENT1 = pygame.USEREVENT + 1
SPAWN_COMET_EVENT2 = pygame.USEREVENT + 2 

pygame.time.set_timer(SPAWN_COMET_EVENT1, random.randint(1, 2) * 1000)
pygame.time.set_timer(SPAWN_COMET_EVENT2, random.randint(1, 3) * 1000)

# Game loop
running = True
while running:
    clock.tick(30)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

    
        # Handle comet spawning
        if event.type == SPAWN_COMET_EVENT2:
            Comet2(groups=all_sprites)  
        if event.type == SPAWN_COMET_EVENT1:
            Comet1(groups=all_sprites)
    



    all_sprites.update()
    

    # Background
    display_surface.fill((0, 0, 0))  # Black background
    
    # Draw stars
    for star, pos in stars:
        display_surface.blit(star, pos)
      
    all_sprites.draw(display_surface)
    
    display_score()
    
    pygame.display.update()

pygame.quit()
