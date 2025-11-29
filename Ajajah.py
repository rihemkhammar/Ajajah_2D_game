import pygame
from sys import exit
import time
import pygame.image
from random import randint

#########################
LandSurface =290
wGame, hGame = 735,440
wGame5 =730
wSnail, hSnail = 40,40
wPlayer, hPlayer = 150,150
#########################
def scroll_images(images_list, positions_list, speeds_list):
    """
    images_list : liste des surfaces pygame
    positions_list : liste de tuples [(x1,y1), (x2,y2), ...]
    speeds_list : liste des vitesses correspondantes à chaque image
    Retourne la nouvelle liste de positions mises à jour
    """
    new_positions = []
    for i, img in enumerate(images_list):
        x, y = positions_list[i]
        speed = speeds_list[i]
        x -= speed
        if x <= -img.get_width():
            x = wGame
        screen.blit(img, (x, y))
        new_positions.append((x, y))

    return new_positions


def display_score ():
    current_time = int(pygame.time.get_ticks()/ 1000)  - start_time
    score_surf = test_font.render(f'Score:{current_time}',False,(0, 0, 128))
    score_rect = score_surf.get_rect(center=(610, 70))
    pygame.draw.rect(screen,'Pink',score_rect,4,5)
    screen.blit(score_surf, score_rect)
    return current_time

def collision_safe(rect1, rect2, marge=20):
    r1 = rect1.inflate(-marge, -marge)  # réduit la zone
    r2 = rect2.inflate(-marge, -marge)
    return r1.colliderect(r2)
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if obstacle_rect.bottom < 320:  # Fly
                if collision_safe(player, obstacle_rect, marge=15):
                    return False
            elif obstacle_rect.bottom == 329:  # Snail
                if collision_safe(player, obstacle_rect, marge=25):
                    return False
            elif 325 <= obstacle_rect.bottom <= 335:  # Bunny
                if collision_safe(player, obstacle_rect, marge=20):
                    return False

    return True



def obstacle_mouvement(obstacle_list):

        if obstacle_list:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x -= 4
                # vérifier quel type d'obstacle c'est
                if obstacle_rect.bottom == 329:
                    screen.blit(snail_surface, obstacle_rect)
                elif obstacle_rect.bottom == 310:
                    screen.blit(fly_surface, obstacle_rect)
                elif obstacle_rect.bottom == 330:
                    screen.blit(bunny_surface, obstacle_rect)
            # enlever les obstacles sortis de l'écran
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
            return obstacle_list
        else:
            return []


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 340:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]



pygame.init()  # initializes all Pygame modules

screen = pygame.display.set_mode((wGame,hGame))
pygame.display.set_caption("Ajajah")
clock = pygame.time.Clock()  #creates a Clock object to control the game's frame rate and ensure smooth, consistent updates.
test_font= pygame.font.Font('font/Super Crawler.ttf', 40)
test_font1= pygame.font.Font('font/Pixel-Regular.ttf', 40)
game_active = False
start_time = 0
score = 0
#houses
# Charger les 3 images
img1 = pygame.image.load('graphics/background/house1.png').convert_alpha()
img2 = pygame.image.load('graphics/background/house2.png').convert_alpha()
img3 = pygame.image.load('graphics/background/house3.png').convert_alpha()
img4 = pygame.image.load('graphics/background/house3.png').convert_alpha()
# Redimension si besoin
img1 = pygame.transform.scale(img1, (120, 120))
img2 = pygame.transform.scale(img2, (150, 150))
img3 = pygame.transform.scale(img3, (100, 100))
img4 = pygame.transform.scale(img3, (100, 100))

images_list = [img1,img4, img2, img3]
positions_list = [(100, 235), (300, 270),(550, 225),(800, 270)]
speeds_list = [2,2 , 2,2]


sky_surface = pygame.image.load('graphics/sky.jpeg').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
text_surface = test_font.render('Ajajah', False, (0, 0, 128))
#score_surf = test_font.render('00', False, (0, 0, 128))
#score_rect = score_surf.get_rect(center = (610, 70))
#obstacle
#snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png' ).convert_alpha()
snail_frame_1 = pygame.transform.scale(snail_frame_1, (40, 40))
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png' ).convert_alpha()
snail_frame_2 = pygame.transform.scale(snail_frame_2, (40, 40))
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]
#snail_rect =snail_surface.get_rect(bottomright= (wGame5,329))
#fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png' ).convert_alpha()
fly_frame_1 = pygame.transform.scale(fly_frame_1, (70, 40))
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png' ).convert_alpha()
fly_frame_2 = pygame.transform.scale(fly_frame_2, (70, 40))
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index =0
fly_surface = fly_frames[fly_frame_index]
# Bunny obstacle
bunny_frame_1 = pygame.image.load('graphics/bunny/bunny1.png').convert_alpha()
bunny_frame_1 = pygame.transform.scale(bunny_frame_1, (60, 60))
bunny_frame_2 = pygame.image.load('graphics/bunny/bunny2.png').convert_alpha()
bunny_frame_2 = pygame.transform.scale(bunny_frame_2, (60, 60))
bunny_frame_3 = pygame.image.load('graphics/bunny/bunny3.png').convert_alpha()
bunny_frame_3 = pygame.transform.scale(bunny_frame_3, (60, 60))
bunny_frame_4 = pygame.image.load('graphics/bunny/bunny4.png').convert_alpha()
bunny_frame_4 = pygame.transform.scale(bunny_frame_4, (60, 60))

bunny_frames = [bunny_frame_1, bunny_frame_2, bunny_frame_3, bunny_frame_4]
bunny_frame_index = 0
bunny_surface = bunny_frames[bunny_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_1 = pygame.transform.scale(player_walk_1, (100, 100))
player_walk_2 = pygame.image.load('graphics/player/player_walk_3.png').convert_alpha()
player_walk_2 = pygame.transform.scale(player_walk_2, (100, 100))
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_jump = pygame.transform.scale(player_jump, (100, 100))
player_surf =player_walk[player_index]
player_rect = player_surf.get_rect(topleft = (80,LandSurface - 50))
player_gravity = 0
#Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand =  pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(topleft = (250,100))
game_message = test_font1.render('Press space to run ', False, (0, 0, 128))
game_message_rect = game_message.get_rect(center = (380,400))

#Timer
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer,1300)

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer,200)
fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,200)
bunny_animation_timer = pygame.USEREVENT + 4
pygame.time.set_timer(bunny_animation_timer, 200)


while True:
    for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            pygame.quit() #properly shuts down all Pygame modules and closes the application.
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) :
                    player_gravity =-20
            if event.type == pygame.KEYDOWN :
               if event.key == pygame.K_SPACE and  player_rect.bottom>= 300:
                   player_gravity = -22
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
                game_active = True
                #snail_rect.left = wGame
                start_time = int(pygame.time.get_ticks()/ 1000)
        if game_active:
            if event.type == obstacle_timer:
                rand_choice = randint(0, 3)
                if rand_choice == 0:
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 329)))
                elif rand_choice == 1:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 310)))
                else:
                    obstacle_rect_list.append(bunny_surface.get_rect(bottomright=(randint(900, 1100), 330)))

            if event.type == snail_animation_timer:
                if snail_frame_index ==0: snail_frame_index =1
                else: snail_frame_index=0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index ==0: fly_frame_index =1
                else: fly_frame_index=0
                fly_surface = fly_frames[fly_frame_index]
            if event.type == bunny_animation_timer:
                bunny_frame_index = (bunny_frame_index + 1) % len(bunny_frames)
                bunny_surface = bunny_frames[bunny_frame_index]

    #Draw all our elementnail
    #static screen
    if game_active:
        screen.blit(sky_surface,(0,0))

        # faire défiler les 3 images
        positions_list = scroll_images(images_list, positions_list, speeds_list)
        screen.blit(ground_surface,(0,329))
        #pygame.draw.rect(screen,'Pink',score_rect,4,5)
        #pygame.draw.ellipse(screen,'Brown',pygame.Rect(50,200,100,100))
        screen.blit(text_surface,(310,35))
        score = display_score()

        #dynamic screen

        #snail_rect.x-= 4
        #if snail_rect.right <= 0 : snail_rect.left = 800
        #screen.blit(snail_surface,snail_rect)
        #player
        player_gravity +=1
        player_rect.y += player_gravity
        if player_rect.bottom >= 340 : player_rect.bottom = 340
        player_animation()
        screen.blit(player_surf,player_rect)

        #Obstacle mouvement
        obstacle_rect_list = obstacle_mouvement(obstacle_rect_list)


        #collision
        game_active = collisions(player_rect,obstacle_rect_list)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,329)
        player_gravity = 0
        score_message = test_font.render(f'Your score: {score}',False,(0, 0, 128))
        score_message_rect = score_message.get_rect(center = (380,400))
        screen.blit(text_surface, (310, 35))
        screen.blit(game_message, game_message_rect) if score == 0 else screen.blit(score_message,score_message_rect)





    keys =  pygame.key.get_pressed( )
    #keys[pygame.K_SPACE]
    #if player_rect.colliderect(snail_rect):

    #mouse_pos = pygame.mouse.get_pos()
    #if player_rect.collidepoint(mouse_pos):
    #    pygame.mouse.get_pressed()



    # update everything
    pygame.display.update()
    clock.tick(60)
