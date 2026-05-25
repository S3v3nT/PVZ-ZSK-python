import pygame
import os
from random import randint, choice
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound
window = pygame.display.set_mode((1400,600))
print("Aktualny katalog roboczy:", os.getcwd())
print("Katalog skryptu:", os.path.dirname(os.path.abspath(__file__)))
scriptDir = os.path.dirname(os.path.abspath(__file__))

class peashooter:
    def __init__(self, x_cord, y_cord):
        self.shoot_cooldown = 0
        self.shoot_rate = 50
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
        self.image = pygame.transform.scale(self.image, (80, 80))  # width, height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))

class peaBall:
    def __init__(self, peashooter):
        self.peashooter = peashooter
        self.x_cord = peashooter.x_cord + 50
        self.y_cord = peashooter.y_cord + 5
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peaBall.png'))
        self.image = pygame.transform.scale(self.image, (30, 30))  # width, height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord + 5, self.y_cord + 5, self.width - 12, self.height - 12)
        
    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))
    
    def move(self):
        self.x_cord += 3
        self.hitbox = pygame.Rect(self.x_cord + 5, self.y_cord + 5, self.width - 12, self.height - 12)
    
    
    def isOffscreen(self):
        return self.x_cord > 1450
    
    def update(self):
        self.move()
        if self.isOffscreen():
            return True
        return False

class zombie:
    def __init__(self, y_cord):
        self.x_cord = 1400
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'zombie.png'))
        self.image = pygame.transform.scale(self.image, (75, 125))
        
        self.hp = 125
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    
    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))
    
    def move(self):
        self.x_cord -= 0.62
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    
def get_wave_count(elapsed_time):
    """Return how many zombies to spawn based on game time"""
    if elapsed_time < 10:
        return 0
    elif elapsed_time < 30:
        return 1  # Wave 1: 1 zombie (10-30 seconds)
    elif elapsed_time < 60:
        return 2
    elif elapsed_time < 120:
        return 3
    elif elapsed_time < 180:
        return 4
    elif elapsed_time < 240:
        return 5
    else:
        return randint(6, 8)

class Sunflower:
    def __init__(self, x_cord, y_cord):
        self.production_cooldown = 100
        self.production_rate = 150
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'sunflowerZsk.png'))
        self.image = pygame.transform.scale(self.image, (100, 100))  # width, height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))

class SunBall:
    def __init__(self, sunflower):
        self.sunflower = sunflower
        self.x_cord = randint(self.sunflower.x_cord - 20, self.sunflower.x_cord + self.sunflower.width + 20)
        self.y_cord = randint(self.sunflower.y_cord - 10, self.sunflower.y_cord + self.sunflower.height + 10)
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'sun.png'))
        self.image = pygame.transform.scale(self.image, (60, 60))
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    
    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))
    
    def is_clicked(self, mouse_pos):
        return self.hitbox.collidepoint(mouse_pos)

class Wallnut:
    def __init__(self, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'wallnut.png'))
        self.image = pygame.transform.scale(self.image, (80, 80))
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    
    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))
    

def main():
    peashooter_place_cooldown = 0
    peashooter_place_rate = 60  # cooldown in frames (60 frames = 1 second at 60 FPS)
    sunflower_place_cooldown = 0
    sunflower_place_rate = 60
    placing_peashooter = False
    placing_sunflower = False
    elapsed_time = 0  # Track seconds elapsed
    # 9x5 tile grid system
    tile_cols = 9
    tile_rows = 5
    tile_width = 80
    tile_height = 100
    grid_start_x = 250
    grid_start_y = 50
    
    # Generate all tile positions
    tile_positions = {}  # (col, row) -> (x, y)
    for col in range(tile_cols):
        for row in range(tile_rows):
            x = grid_start_x + col * tile_width
            y = grid_start_y + row * tile_height
            tile_positions[(col, row)] = (x, y)
    
    occupied_tiles = {}  # (col, row) -> peashooter object
    
    run = True
    hitboxes = False
    game_over = False
    peaballs = []
    sunflowers = []
    wallnuts = []
    zombies = []
    suns = []
    score = 0
    sunCurrency = 25
    
    peashooter_card = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterCard.png'))
    peashooter_card = pygame.transform.scale(peashooter_card, (80, 100))
    peaShooterCard_rect = peashooter_card.get_rect(topleft=(20, 100))
    
    sunflower_card = pygame.image.load(os.path.join(scriptDir, 'assets', 'sunflowerCard.png'))
    sunflower_card = pygame.transform.scale(sunflower_card, (80, 100))
    sunflowerCard_rect = sunflower_card.get_rect(topleft=(20, 220))
    
    
        
    font = pygame.font.SysFont(None, 36)
    bigFont = pygame.font.SysFont(None, 70)
    
    clock = pygame.time.Clock()
    
    background = pygame.image.load(os.path.join(scriptDir, 'assets', 'ogrod.jpg'))
    scoreCooldown = 0
    scoreRate = 60
    
    zombie_cooldown = 0
    zombie_rate = 60
    
    peashooter_place_cooldown = 0
    peashooter_place_rate = 240
    
    sunflower_place_cooldown = 0
    sunflower_place_rate = 120

    pygame.mixer.music.load(os.path.join(scriptDir, 'assets', 'zombies.mp3'))
    pygame.mixer.music.play(0)
    pygame.mixer.music.set_volume(1)

    while run:
        clock.tick(60) 
        elapsed_time += 1/60 
        pygame.time.Clock().tick(60)
        if elapsed_time > 4:  # Start music after 2 seconds
           if not pygame.mixer.music.get_busy():
               pygame.mixer.music.load(os.path.join(scriptDir, 'assets', 'theme_music.mp3'))
               pygame.mixer.music.play(-1)
               pygame.mixer.music.set_volume(0.075)  # Set volume to 50% (adjust 0-1)
        if peashooter_place_cooldown > 0:
           peashooter_place_cooldown -= 1
    
        if sunflower_place_cooldown > 0:
           sunflower_place_cooldown -= 1
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    hitboxes = not hitboxes
                
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        return main()
                    elif event.key == pygame.K_q:
                        run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                clicked_sun = False
                for sun in suns[:]:
                    if sun.is_clicked(event.pos):
                        sunCurrency += 25
                        suns.remove(sun)
                        clicked_sun = True
                        break

                if clicked_sun:
                    continue

                if sunflowerCard_rect.collidepoint(event.pos) and sunCurrency >= 25 and sunflower_place_cooldown == 0:
                    placing_sunflower = True  
                    placing_peashooter = False
                    peashooter_card.set_alpha(255)
               
                elif placing_sunflower:  
                    mouse_x, mouse_y = event.pos
                    clicked_col = None
                    clicked_row = None
                   
                    for col in range(tile_cols):
                        if grid_start_x + col * tile_width <= mouse_x < grid_start_x + (col + 1) * tile_width:
                           clicked_col = col
                           break
                   
                    for row in range(tile_rows):
                        if grid_start_y + row * tile_height <= mouse_y < grid_start_y + (row + 1) * tile_height:
                           clicked_row = row
                           break
                   
                    if clicked_col is not None and clicked_row is not None:
                        if (clicked_col, clicked_row) not in occupied_tiles:
                            x, y = tile_positions[(clicked_col, clicked_row)]
                            occupied_tiles[(clicked_col, clicked_row)] = Sunflower(x, y)
                            sunCurrency -= 25
                            sunflower_place_cooldown = sunflower_place_rate
                        placing_sunflower = False  

                elif peaShooterCard_rect.collidepoint(event.pos) and sunCurrency >= 100 and peashooter_place_cooldown == 0:
                    placing_peashooter = True  
                    placing_sunflower = False
                    sunflower_card.set_alpha(255)
               
                elif placing_peashooter:  
                    mouse_x, mouse_y = event.pos
                    clicked_col = None
                    clicked_row = None
                   
                    for col in range(tile_cols):
                        if grid_start_x + col * tile_width <= mouse_x < grid_start_x + (col + 1) * tile_width:
                           clicked_col = col
                           break
                   
                    for row in range(tile_rows):
                        if grid_start_y + row * tile_height <= mouse_y < grid_start_y + (row + 1) * tile_height:
                           clicked_row = row
                           break
                   
                    if clicked_col is not None and clicked_row is not None:
                        if (clicked_col, clicked_row) not in occupied_tiles:
                            x, y = tile_positions[(clicked_col, clicked_row)]
                            occupied_tiles[(clicked_col, clicked_row)] = peashooter(x, y)
                            sunCurrency -= 100
                            peashooter_place_cooldown = peashooter_place_rate
                        placing_peashooter = False
        
        keys = pygame.key.get_pressed()
        
        if not game_over:
            for tile_pos, plant in occupied_tiles.items():
                if isinstance(plant, peashooter):
                    if plant.shoot_cooldown > 0:
                        plant.shoot_cooldown -= 0.5

                    if plant.shoot_cooldown == 0:
                        for zomb in zombies:
                            if abs(zomb.y_cord - plant.y_cord) < 100:  
                                peaballs.append(peaBall(plant))
                                plant.shoot_cooldown = plant.shoot_rate  
                                break
                                
                elif isinstance(plant, Sunflower):
                    if plant.production_cooldown > 0:
                        plant.production_cooldown -= 1
                    
                    if plant.production_cooldown == 0:
                        suns.append(SunBall(plant))
                        sunflower_count = sum(1 for p in occupied_tiles.values() if isinstance(p, Sunflower))
                        sunflower_penalty = 20
                        plant.production_cooldown = min(480, plant.production_rate + (sunflower_count * sunflower_penalty))
            
            # Spawn zombies
            if zombie_cooldown > 0:
                zombie_cooldown -= 0.5
            
            if zombie_cooldown == 0:
                wave_count = get_wave_count(elapsed_time)
                for _ in range(wave_count):
                    random_row = randint(0, tile_rows - 1)
                    y = grid_start_y + random_row * tile_height
                    zombies.append(zombie(y))
                
                zombie_rate = max(20, 100 - (score // 100))
                zombie_cooldown = zombie_rate
            
            # Update peaballs and check collision with zombies
            for peaball in peaballs[:]:
                is_offscreen = peaball.update()

                if is_offscreen:
                    if peaball in peaballs:
                        peaballs.remove(peaball)
                    continue
                
                # Check collision with zombies
                for zomb in zombies[:]:
                    if peaball.hitbox.colliderect(zomb.hitbox):
                        zomb.hp -= 25
                        if zomb.hp <= 0:
                            zombies.remove(zomb)
                            score += 50
                        if peaball in peaballs:
                            peaballs.remove(peaball)
                        break
            
            # Move zombies
            for zomb in zombies[:]:
                zomb.move()
                # Check if zombie reached the house (behind peashooters)
                if zomb.x_cord < 200:
                    game_over = True
                if zomb.x_cord < 0:
                    if zomb in zombies:
                        zombies.remove(zomb)
            
            if scoreCooldown > 0:
                scoreCooldown -= 1
            
            if scoreCooldown == 0:
                score += 1
                scoreCooldown = scoreRate
            
        window.blit(background,(0,0))
        
        # Update card transparency based on cooldown and placing state
        if peashooter_place_cooldown > 0:
            peashooter_alpha = int(255 * (1 - peashooter_place_cooldown / peashooter_place_rate))
            peashooter_card.set_alpha(peashooter_alpha)
        elif placing_peashooter:
            peashooter_card.set_alpha(180)
        else:
            peashooter_card.set_alpha(255)
        
        if sunflower_place_cooldown > 0:
            sunflower_alpha = int(255 * (1 - sunflower_place_cooldown / sunflower_place_rate))
            sunflower_card.set_alpha(sunflower_alpha)
        elif placing_sunflower:
            sunflower_card.set_alpha(180)
        else:
            sunflower_card.set_alpha(255)
        
        window.blit(peashooter_card, peaShooterCard_rect)
        window.blit(sunflower_card, sunflowerCard_rect)
        
        for peaball in peaballs:
            peaball.draw()
        
        for zomb in zombies:
            zomb.draw()
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (20, 20))
        
        sunCurrency_text = font.render(f"Suns: {sunCurrency}", True, (255, 255, 255))
        window.blit(sunCurrency_text, (20, 75))
        
        for tile_pos, plant in occupied_tiles.items():
            plant.draw()
        
        for tile_pos, pea in occupied_tiles.items():
            pea.draw()
        
        for tile_pos, sunflowers in occupied_tiles.items():
            sunflowers.draw()
        
        for sun in suns:
            sun.draw()
        
        if placing_peashooter:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if cursor is in any tile
            for col in range(tile_cols):
                for row in range(tile_rows):
                    if (grid_start_x + col * tile_width <= mouse_x < grid_start_x + (col + 1) * tile_width and
                        grid_start_y + row * tile_height <= mouse_y < grid_start_y + (row + 1) * tile_height):
                        if (col, row) not in occupied_tiles:
                            preview_image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
                            preview_image = pygame.transform.scale(preview_image, (80, 80))
                            preview_image.set_alpha(180)  # 50% transparent
                            x, y = tile_positions[(col, row)]
                            window.blit(preview_image, (x, y))  # Show at tile position
                        break
        
        if placing_sunflower:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if cursor is in any tile
            for col in range(tile_cols):
                for row in range(tile_rows):
                    if (grid_start_x + col * tile_width <= mouse_x < grid_start_x + (col + 1) * tile_width and
                        grid_start_y + row * tile_height <= mouse_y < grid_start_y + (row + 1) * tile_height):
                        if (col, row) not in occupied_tiles:
                            preview_image = pygame.image.load(os.path.join(scriptDir, 'assets', 'sunflowerZsk.png'))
                            preview_image = pygame.transform.scale(preview_image, (80, 80))
                            preview_image.set_alpha(180)  # 50% transparent
                            x, y = tile_positions[(col, row)]
                            window.blit(preview_image, (x, y))  # Show at tile position
                        break
        
        if hitboxes:
            for peaball in peaballs[:]:
                pygame.draw.rect(window, (0, 100, 255), peaball.hitbox, 2)
        
            for zomb in zombies[:]:
                pygame.draw.rect(window, (0, 255, 0), zomb.hitbox, 2)
            
            for sun in suns[:]:
                pygame.draw.rect(window, (0, 100, 255), sun.hitbox, 2)
            
            for tile_pos, pea in occupied_tiles.items():
                pygame.draw.rect(window, (0, 100, 255), pea.hitbox, 2)
        
            # Draw tile hitboxes
            for col in range(tile_cols):
                for row in range(tile_rows):
                    x = grid_start_x + col * tile_width
                    y = grid_start_y + row * tile_height
                    tile_rect = pygame.Rect(x, y, tile_width, tile_height)
                    pygame.draw.rect(window, (255, 0, 0), tile_rect, 1)
        
        # Display game over screen
        if game_over:
            overlay = pygame.Surface((1400, 600))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            window.blit(overlay, (0, 0))
            
            game_over_text = bigFont.render("GAME OVER", True, (255, 0, 0))
            final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
            
            game_over_rect = game_over_text.get_rect(center=(700, 200))
            score_rect = final_score_text.get_rect(center=(700, 300))
            restart_rect = restart_text.get_rect(center=(700, 400))
            
            window.blit(game_over_text, game_over_rect)
            window.blit(final_score_text, score_rect)
            window.blit(restart_text, restart_rect)
        
        pygame.display.update()

if __name__== "__main__":
    main()