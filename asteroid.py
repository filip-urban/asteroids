import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen, (255, 255, 255), (self.position), self.radius, width=2
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self, asteroid_field):
        if self.radius > ASTEROID_MIN_RADIUS:
            new_velocity = 1.2 * self.velocity.rotate(random.uniform(20, 50))
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid_field.spawn(
                new_radius,
                self.position,
                new_velocity,
            )
            asteroid_field.spawn(
                new_radius,
                self.position,
                -new_velocity,
            )
        self.kill()

    def bounce(self, other):
        # calculate angle of the new vector and rotate the velocity vektor by this angle
        new_angle = self.position.angle_to(
            1.2 * pygame.Vector2(self.position.x - other.x, self.position.y - other.y)
        )
        self.velocity = self.velocity.rotate(new_angle)
