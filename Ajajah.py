import pygame
from sys import exit
import pygame.image
from random import choice
import json
from player import Player
from obstacle import Obstacle
from house import House

#########################
LandSurface = 290
wGame, hGame = 735, 440
wGame5 = 730
wSnail, hSnail = 40, 40
wPlayer, hPlayer = 150, 150
#########################


# --- HELPER FUNCTIONS ---
def display_score(screen, test_font, start_time):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (0, 0, 128))
    score_rect = score_surf.get_rect(center=(610, 70))
    pygame.draw.rect(screen, 'Pink', score_rect, 4, 5)
    screen.blit(score_surf, score_rect)
    return current_time

def collision_safe(rect1, rect2, marge=20):
    r1 = rect1.inflate(-marge, -marge)
    r2 = rect2.inflate(-marge, -marge)
    return r1.colliderect(r2)

def custom_collide(player_sprite, obstacle_sprite, marge=20):
    return collision_safe(player_sprite.rect, obstacle_sprite.rect, marge)

def collision_sprite(player_group, obstacle_group):
    for obstacle in obstacle_group:
        if custom_collide(player_group.sprite, obstacle, marge=20):
            obstacle_group.empty()
            return False
    return True

# --- MAIN FUNCTION ---
def main():
    with open('obstacle_data.json', 'r') as f:
        OBSTACLE_DATA = json.load(f)
    with open('background_data.json', 'r') as f:
        BACKGROUND_DATA = json.load(f)
    with open('player_data.json', 'r') as f:
        PLAYER_DATA = json.load(f)

    PLAYER_DATA['size'] = tuple(PLAYER_DATA['size'])
    PLAYER_DATA['start_pos'] = tuple(PLAYER_DATA['start_pos'])
    for obstacle in OBSTACLE_DATA.values():
        obstacle['size'] = tuple(obstacle['size'])

    # --- Initialize Pygame ---
    pygame.init()
    screen = pygame.display.set_mode((wGame, hGame))
    pygame.display.set_caption("Ajajah")
    clock = pygame.time.Clock()
    test_font = pygame.font.Font('font/Super Crawler.ttf', 40)
    test_font1 = pygame.font.Font('font/Pixel-Regular.ttf', 40)

    game_active = False
    start_time = 0
    score = 0

    # --- Groups ---
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Player(
        walk_paths=PLAYER_DATA['walk_paths'],
        jump_path=PLAYER_DATA['jump_path'],
        size=PLAYER_DATA['size'],
        pos=PLAYER_DATA['start_pos']
    ))

    obstacle_group = pygame.sprite.Group()
    house_group = pygame.sprite.Group()
    for house in BACKGROUND_DATA['houses']:
        pos = tuple(house['pos'])
        size = tuple(house['size'])
        house_group.add(House(house['image_path'], pos, size, house['speed']))

    # --- Load sky and ground ---
    sky_surface = pygame.image.load(BACKGROUND_DATA['sky']['image_path']).convert()
    sky_surface = pygame.transform.scale(sky_surface, tuple(BACKGROUND_DATA['sky']['size']))

    ground_surface = pygame.image.load(BACKGROUND_DATA['ground']['image_path']).convert_alpha()
    ground_surface = pygame.transform.scale(ground_surface, tuple(BACKGROUND_DATA['ground']['size']))

    text_surface = test_font.render('Ajajah', False, (0, 0, 128))

    # --- Intro screen ---
    player_stand = pygame.image.load(PLAYER_DATA['stand_path']).convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect = player_stand.get_rect(topleft=(250, 100))
    game_message = test_font1.render('Press space to run', False, (0, 0, 128))
    game_message_rect = game_message.get_rect(center=(380, 400))

    # --- Timer ---
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1300)

    # --- Main loop ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # --- Player input ---
            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_group.sprite.rect.collidepoint(event.pos):
                        player_group.sprite.gravity = -20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_group.sprite.rect.bottom >= 300:
                        player_group.sprite.gravity = -22
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

            # --- Spawn obstacles ---
            if game_active and event.type == obstacle_timer:
                type_choice = choice(list(OBSTACLE_DATA.keys()))
                data = OBSTACLE_DATA[type_choice]
                obstacle_group.add(Obstacle(type_choice, data['paths'], data['size'], data['y']))

        # --- Game update ---
        if game_active:
            screen.blit(sky_surface, (0, 0))
            house_group.update()
            house_group.draw(screen)
            screen.blit(ground_surface, (0, 329))
            screen.blit(text_surface, (310, 35))
            score = display_score(screen, test_font, start_time)

            player_group.draw(screen)
            player_group.update()
            obstacle_group.draw(screen)
            obstacle_group.update()
            game_active = collision_sprite(player_group, obstacle_group)
        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)
            player_group.sprite.rect.midbottom = (80, 329)
            player_group.sprite.gravity = 0
            score_message = test_font.render(f'Your score: {score}', False, (0, 0, 128))
            score_message_rect = score_message.get_rect(center=(380, 400))
            screen.blit(text_surface, (310, 35))
            screen.blit(game_message, game_message_rect) if score == 0 else screen.blit(score_message, score_message_rect)

        # --- Update display ---
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
