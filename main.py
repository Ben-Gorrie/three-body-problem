import pyglet

window = pyglet.window.Window()

# Batch to group planets together
batch = pyglet.graphics.Batch()

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
    ):
        self.x, self.y = starting_pos


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()
