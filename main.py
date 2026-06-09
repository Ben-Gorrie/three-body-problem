import pyglet
import numpy as np

window = pyglet.window.Window()

# Batch to group planets together
batch = pyglet.graphics.Batch()

dt = 0.1
G = 6.674 * 10 ** (-11)

planet1 = pyglet.shapes.Circle(
    x=window.width // 2,
    y=(2 * window.height) // 3,
    radius=10,
    color=(255, 0, 0),
    batch=batch,
)

planet2 = pyglet.shapes.Circle(
    x=window.width // 3,
    y=window.height // 3,
    radius=10,
    color=(0, 255, 0),
    batch=batch,
)

planet3 = pyglet.shapes.Circle(
    x=(2 * window.width) // 3,
    y=window.height // 3,
    radius=10,
    color=(0, 0, 255),
    batch=batch,
)


class Planet:
    def __init__(
        self,
        starting_pos: tuple[float, float],
        starting_v: tuple[float, float],
        starting_a: tuple[float, float],
        mass: float,
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

    # Compute the displacement at x(t + dt) using the velocity verlet from https://en.wikipedia.org/wiki/Verlet_integration#Velocity_Verlet
    def compute_next_displacement(self):
        self.x_dt = self.x + self.v * dt + 0.5 * self.a * dt**2

    def compute_next_acceleration(self, other_planets: list[Planet]):
        total_a = 0

        for planet in other_planets:
            total_a += (G * planet.m) / (self.x_dt - planet.x_dt) ** 2

        self.a_dt = total_a

    def compute_next_velocity(self):
        self.v_dt = self.v + 0.5 * (self.a + self.a_dt) * dt


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()
