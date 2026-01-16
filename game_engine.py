import time
import math
import pygame
from pygame import Vector2

from characters import Character
from utils import GameField

class GameEngine:
    def __init__(self, graph_engine, game_field, player, npcs, *, fps=60):

        self.graph_engine = graph_engine

        self.game_field = game_field
        self.player = player
        self.npcs = npcs
        self.fps = fps

    def update_state(self, keys):
        for i in range(len(self.npcs)):
            self.npcs[i].move()

        self.player.move(keys[pygame.K_a], keys[pygame.K_d],
                         keys[pygame.K_w], keys[pygame.K_s])
        
        bottom_left = Vector2(self.game_field.x_min, self.game_field.y_min)
        bottom_right = Vector2(self.game_field.x_max, self.game_field.y_min)
        top_right = Vector2(self.game_field.x_max, self.game_field.y_max)
        top_left = Vector2(self.game_field.x_min, self.game_field.y_max)

        walls = [(bottom_left, bottom_right), (bottom_right, top_right),
                 (top_right, top_left), (top_left, bottom_left)]

        ITER = 10
        for _ in range(ITER):
            for i in range(len(self.npcs)):
                self.handle_collision(self.player, self.npcs[i])
                for j in range(i, len(self.npcs)):
                    self.handle_collision(self.npcs[i], self.npcs[j])
            
            for wall_a, wall_b in walls:
                self.handle_wall_collision(self.player, wall_a, wall_b)
                for i in range(len(self.npcs)):
                    self.handle_wall_collision(self.npcs[i], wall_a, wall_b)

        if keys[pygame.K_q]:
            self.running = False
    
    def handle_collision(self, char_1: Character, char_2: Character, slop=0.01, percent=0.8):
        delta = char_1.pos - char_2.pos
        dist = delta.length()
        sum_of_radii = char_1.radius + char_2.radius

        if dist >= sum_of_radii:
            return False  # no overlap 

        if dist == 0:
            collision_normal = Vector2(1, 0)  # avoid division by zero in the following
        else:
            collision_normal = delta / dist
        
        # --- 1) Position correction ("Baumgarte stabilization" preventing overlaps)
        penetration = sum_of_radii - dist

        inv_mass_1 = 0.0 if char_1.mass == 0 else 1.0 / char_1.mass
        inv_mass_2 = 0.0 if char_2.mass == 0 else 1.0/ char_2.mass
        inv_mass_sum = inv_mass_1 + inv_mass_2

        if inv_mass_sum == 0.0:
            return True  # both immovable but overlapping; nothing to do
        
        # prevent jittering (somehow)
        correction_mag = max(penetration - slop, 0.0) * percent / inv_mass_sum
        correction = correction_mag * collision_normal

        # TODO: Tune the number of iterations which may be too low.
        char_1.pos += correction * inv_mass_1
        char_2.pos -= correction * inv_mass_2

        # --- 2) Velocity update according to conservation of momentum
        vel_diff = char_1.vel - char_2.vel
        normal_vel = vel_diff.dot(collision_normal)

        # If characters are already separating no need for an update.
        if normal_vel > 0:
            return True
        
        e = 0.5  # coefficient of restitution
        impulse_mag = - (1 + e) * normal_vel / inv_mass_sum
        impulse = impulse_mag * collision_normal
        char_1.vel += impulse * inv_mass_1
        char_2.vel -= impulse * inv_mass_2

        return True
    

    def handle_wall_collision(self, char: Character, wall_a: Vector2, wall_b: Vector2, 
                              slop=0.01, percent=0.8):
        wall_segment = wall_b - wall_a

        # Closest point on wall segment to charecter
        t = (char.pos - wall_a).dot(wall_segment) / (wall_segment.length() ** 2)
        t = max(0.0, min(1.0, t))
        C = wall_a + t * wall_segment

        # Vector from closest point to center
        delta = char.pos - C
        if delta.length() >= char.radius:
            return False  # no collision
        
        if delta.length() == 0:
            collision_normal = Vector2(-wall_segment.y, wall_segment.x)
            if collision_normal.length() == 0:
                collision_normal = Vector2(1, 0)
            else:
                collision_normal = collision_normal.normalize()
        else:
            collision_normal = delta / delta.length()
        
        # --- 1) Positional correction
        penetration = char.radius - delta.length()
        correction_mag = max(penetration - slop, 0.0) * percent
        char.pos += collision_normal * correction_mag

        # --- 2) Velocity update
        normal_vel = char.vel.dot(collision_normal)

        if normal_vel < 0:
            # bouncing into a wall
            e = 0.5  # restitution
            char.vel += - (1.0 + e) * normal_vel * collision_normal

        return True


    def render_state(self):
        self.graph_engine.start_frame()

        self.graph_engine.render_circle(
            self.player.pos, self.player.radius, "red")
        
        for npc in self.npcs:
            self.graph_engine.render_circle(npc.pos, npc.radius, "blue")

        self.graph_engine.show_frame()

    # def subscribe_events(self):

    def run_game(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.update_state(keys)
            self.render_state()
            pygame.display.flip()

            time.sleep(1 / self.fps)
