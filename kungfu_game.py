import pygame
import sys
import webbrowser

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

PLAYER_COLORS = [RED, BLUE, GREEN]

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True

    def move(self, keys, left, right, jump):
        speed = 5
        if keys[left]:
            self.vel_x = -speed
        elif keys[right]:
            self.vel_x = speed
        else:
            self.vel_x = 0
        if keys[jump] and self.on_ground:
            self.vel_y = -12
            self.on_ground = False

    def update(self):
        gravity = 0.5
        self.vel_y += gravity
        self.x += self.vel_x
        self.y += self.vel_y
        if self.y + self.height >= SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50 - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def attack(self, attack_type):
        print(f"Player attack: {attack_type}")


def open_github():
    webbrowser.open_new_tab("https://github.com/NotMarketablePlayer123")


def open_youtube():
    webbrowser.open_new_tab("https://www.youtube.com/@NotMarketablePlayer123")


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kung Fu Game")
    clock = pygame.time.Clock()

    current_scene = "title"
    color_index_p1 = 0
    color_index_p2 = 1

    player1 = Player(200, SCREEN_HEIGHT - 150, PLAYER_COLORS[color_index_p1])
    player2 = Player(560, SCREEN_HEIGHT - 150, PLAYER_COLORS[color_index_p2])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if current_scene == "title":
                    if event.key == pygame.K_1:
                        current_scene = "game"
                    elif event.key == pygame.K_2:
                        current_scene = "how"
                    elif event.key == pygame.K_3:
                        current_scene = "settings"
                    elif event.key == pygame.K_4:
                        open_github()
                    elif event.key == pygame.K_5:
                        open_youtube()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif current_scene == "how":
                    if event.key == pygame.K_ESCAPE:
                        current_scene = "title"
                elif current_scene == "settings":
                    if event.key == pygame.K_a:
                        color_index_p1 = (color_index_p1 + 1) % len(PLAYER_COLORS)
                        player1.color = PLAYER_COLORS[color_index_p1]
                    if event.key == pygame.K_l:
                        color_index_p2 = (color_index_p2 + 1) % len(PLAYER_COLORS)
                        player2.color = PLAYER_COLORS[color_index_p2]
                    if event.key == pygame.K_ESCAPE:
                        current_scene = "title"
                elif current_scene == "game":
                    if event.key == pygame.K_ESCAPE:
                        current_scene = "title"
                    # Attacks
                    if event.key == pygame.K_f:
                        player1.attack("Punch")
                    if event.key == pygame.K_g:
                        player1.attack("Kick")
                    if event.key == pygame.K_h:
                        player1.attack("Chop")
                    if event.key == pygame.K_k:
                        player2.attack("Punch")
                    if event.key == pygame.K_l:
                        player2.attack("Kick")
                    if event.key == pygame.K_SEMICOLON:
                        player2.attack("Chop")

        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        if current_scene == "title":
            draw_text(screen, "Kung Fu Game", 60, SCREEN_WIDTH//2, 80)
            draw_text(screen, "1. Start Game", 40, SCREEN_WIDTH//2, 200)
            draw_text(screen, "2. How To Play", 40, SCREEN_WIDTH//2, 260)
            draw_text(screen, "3. Settings", 40, SCREEN_WIDTH//2, 320)
            draw_text(screen, "4. GitHub", 40, SCREEN_WIDTH//2, 380)
            draw_text(screen, "5. YouTube", 40, SCREEN_WIDTH//2, 440)
            draw_text(screen, "Esc. Quit", 40, SCREEN_WIDTH//2, 500)
        elif current_scene == "how":
            draw_text(screen, "How To Play", 60, SCREEN_WIDTH//2, 80)
            draw_text(screen, "Player 1: Move A/D, Jump W", 30, SCREEN_WIDTH//2, 180)
            draw_text(screen, "F Punch, G Kick, H Chop", 30, SCREEN_WIDTH//2, 220)
            draw_text(screen, "Player 2: Move Left/Right, Jump Up", 30, SCREEN_WIDTH//2, 260)
            draw_text(screen, "K Punch, L Kick, ; Chop", 30, SCREEN_WIDTH//2, 300)
            draw_text(screen, "Esc. Back", 30, SCREEN_WIDTH//2, 360)
        elif current_scene == "settings":
            draw_text(screen, "Settings", 60, SCREEN_WIDTH//2, 80)
            draw_text(screen, "Press A to change Player 1 color", 30, SCREEN_WIDTH//2, 200)
            draw_text(screen, "Press L to change Player 2 color", 30, SCREEN_WIDTH//2, 240)
            draw_text(screen, "Esc. Back", 30, SCREEN_WIDTH//2, 300)
        elif current_scene == "game":
            player1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w)
            player2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)

            player1.update()
            player2.update()

            player1.draw(screen)
            player2.draw(screen)

            draw_text(screen, "Esc. Back to Menu", 30, SCREEN_WIDTH//2, 30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
