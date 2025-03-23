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
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = new_velocity
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = -new_velocity
        self.kill()

    def bounce(self, other):
        vector_to_other = pygame.Vector2(
            self.position.x - other.position.x, self.position.y - other.position.y
        )
        new_angle = self.position.angle_to(vector_to_other)
        overlap = (self.radius + other.radius) - self.position.distance_to(
            other.position
        )
        self.velocity = self.velocity.rotate(new_angle)
        vector_to_other.scale_to_length(1.1 * overlap / 2)
        self.position += vector_to_other
        other.position -= vector_to_other
