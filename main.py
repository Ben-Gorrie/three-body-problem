import pyglet
import numpy as np
from pyglet.window import mouse
from pyglet.window import key

# Main window
window = pyglet.window.Window(fullscreen=True)

# FPS tracker
fps_display = pyglet.window.FPSDisplay(window=window, color=(0, 255, 0, 200))

# Batch to group drawing planets together
batch = pyglet.graphics.Batch()

dt = 1/60.0
G = 300


class Planet:
    def __init__(
        self,
        starting_pos: tuple[float, float],
        starting_v: tuple[float, float],
        starting_a: tuple[float, float],
        mass: float,
        radius: int,
        color: tuple[int, int, int],
        batch,
    ):
        # x and x_dt represents x(t) and x(t + dt)
        self.x = np.array(starting_pos)

        # Initiated to 0 as will be calculated in future
        self.x_dt = 0

        self.v = np.array(starting_v)
        self.v_dt = 0

        self.a = np.array(starting_a)
        self.a_dt = 0

        self.m = mass

        self.radius = radius

        # Graphical representation
        self.circle = pyglet.shapes.Circle(
            x=self.x[0], y=self.x[1], radius=radius, color=color, batch=batch
        )

    # Compute the displacement at x(t + dt) using the velocity verlet from https://en.wikipedia.org/wiki/Verlet_integration#Velocity_Verlet
    def compute_next_displacement(self, dt):
        self.x_dt = self.x + self.v * dt + 0.5 * self.a * dt**2

    # Compute the acceleration at a(t + dt). This uses newton's law of universal gravitation
    def compute_next_acceleration(self, all_planets: list[Planet]):
        total_a = 0

        for planet in all_planets:
            if planet is not self:
                r = planet.x_dt - self.x_dt
                epsilon = planet.radius + self.radius

                dist_sq = np.dot(r, r) + epsilon**2

                total_a += G * planet.m * r / dist_sq**1.5

        self.a_dt = total_a

    # Compute the velocity at v(t + dt)
    def compute_next_velocity(self, dt):
        self.v_dt = self.v + 0.5 * (self.a + self.a_dt) * dt

    def set_current_params(self):
        self.x = self.x_dt
        self.v = self.v_dt
        self.a = self.a_dt

    def update_graphics(self):
        self.circle.x = self.x[0]
        self.circle.y = self.x[1]



p1 = Planet(
    starting_pos=(window.width // 2, (2 * window.height) // 3),
    starting_v=(10, 0),
    starting_a=(1, 0),
    mass=1000,
    radius=10,
    color=(255, 0, 0),
    batch=batch,
)

p2 = Planet(
    starting_pos=(window.width // 3, window.height // 3),
    starting_v=(0, 10),
    starting_a=(0, 1),
    mass=1000,
    radius=10,
    color=(0, 255, 0),
    batch=batch,
)

p3 = Planet(
    starting_pos=((2 * window.width) // 3, window.height // 3),
    starting_v=(0, -10),
    starting_a=(0, -1),
    mass=1000,
    radius=10,
    color=(0, 0, 255),
    batch=batch,
)

p4 = Planet(
    starting_pos=((2.5 * window.width) // 3, window.height // 3),
    starting_v=(0, 0),
    starting_a=(0, 1),
    mass=1000,
    radius=10,
    color=(0, 255, 255),
    batch=batch,
)

planets = [p1, p2, p3, p4]

def update(dt):
    for planet in planets:
        planet.compute_next_displacement(dt)
        planet.compute_next_acceleration(planets)
        planet.compute_next_velocity(dt)
        planet.set_current_params()
        planet.update_graphics()

pyglet.clock.schedule_interval(update, dt)

def spawn_planet(x, y):
    p = Planet(
        starting_pos = (x, y),
        starting_v = (1, 1),
        starting_a = (0, 0),
        mass = 1000,
        radius = 10,
        color = (int((x / window.width) * 255), int((y / window.height) * 255), 0),
        batch = batch,
    )

    planets.append(p)

@window.event
def on_mouse_press(x, y, button, modifiers):
    spawn_planet(x, y)
    print("Spawning planet")

@window.event
def on_key_press(symbol, modifiers):
    # Spawn a sun in the middle of the screen if the s key is pressed
    if symbol == key.S:

        p = Planet(
            starting_pos = (window.width // 2, window.height // 2),
            starting_v = (0, 0),
            starting_a = (0, 0),
            mass = 20000,
            radius = 30,
            color = (255, 255, 0),
            batch = batch,
        )

        planets.append(p)
        print("Spawning Sun")

@window.event
def on_draw():
    window.clear()
    batch.draw()

    # Show FPS
    fps_display.draw() 

pyglet.app.run()
