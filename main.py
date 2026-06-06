import pyglet

window = pyglet.window.Window()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

circle = pyglet.shapes.Circle(x=300, y=300, radius=100, color=(50, 225, 30))


@window.event
def on_draw():
    window.clear()
    label.draw()
    circle.draw()

pyglet.app.run()
