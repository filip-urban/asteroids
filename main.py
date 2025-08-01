import pygame
import pygame.freetype
from constants import *
from player import Player
from shot import Shot
from asteroidfield import AsteroidField, Asteroid


def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    # window name
    pygame.display.set_caption("Asteroids")
    # surface
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    color = (0, 0, 0)
    # clock
    clock = pygame.time.Clock()
    dt = 0
    # font
    font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    # asteroids
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    # player
    Player.containers = (updatable, drawable)
    # Shots
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # score
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill(color)
        updatable.update(dt)
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                player.get_hit()
                asteroid.bounce(player)
                if not player.has_lives():
                    print("Game over!")
                    return

            for other_asteroid in asteroids:
                if asteroid == other_asteroid:
                    continue
                if asteroid.check_collision(other_asteroid):
                    asteroid.bounce(other_asteroid)
                    other_asteroid.bounce(asteroid)

            for shot in shots:
                if asteroid.check_collision(shot):
                    asteroid.split()
                    shot.kill()
                    score += 1
                    break

        for drawable_object in drawable:
            drawable_object.draw(screen)

        # text showing lives
        lives_text = font.render(f"Lives: {player.lives}", True, "white")
        text_rectangle_lives = lives_text.get_rect()
        text_rectangle_lives.center = (SCREEN_WIDTH * 0.92, SCREEN_HEIGHT * 0.06)
        screen.blit(lives_text, text_rectangle_lives)

        # text showing score
        score_text = font.render(f"Score: {score}", True, "white")
        text_rectangle_score = score_text.get_rect()
        text_rectangle_score.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.06)
        screen.blit(score_text, text_rectangle_score)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
