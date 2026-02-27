from . import models
from pyglet.math import Mat4, Vec3
from imptux.renderer import renderer


class Camera(object):
    def __init__(self):
        self.fieldofview = 60
        self.clipnear = 0.1
        self.clipfar = 8192
        self.x = 0
        self.y = 0
        self.z = 512
        self.rx = 0
        self.ry = 0
        self.rz = 0

    def defaultView(self, width, height):
        self.width = width
        self.height = height
        renderer.ctx.viewport = (0, 0, width, height)
        renderer.projection = Mat4.perspective_projection(
            width / height, self.clipnear, self.clipfar, self.fieldofview
        )

    def update(self, dt=0):
        pass

    def position(self, target=None):
        import math
        if target:
            view = Mat4.look_at(
                Vec3(self.x, self.y, self.z),
                Vec3(*target),
                Vec3(0, 1, 0),
            )
        else:
            # Compose translation + rotations (rx, ry, rz)
            view = Mat4.from_translation(Vec3(-self.x, -self.y, -self.z))
            if self.rx:
                view = view @ Mat4.from_rotation(math.radians(self.rx), Vec3(1, 0, 0))
            if self.ry:
                view = view @ Mat4.from_rotation(math.radians(self.ry), Vec3(0, 1, 0))
            if self.rz:
                view = view @ Mat4.from_rotation(math.radians(self.rz), Vec3(0, 0, 1))
        renderer.matrix_stack.load_identity()
        renderer.matrix_stack._stack[-1] = view


class Axis(object):
    def __init__(self, x=0, y=0, z=0, size=100):
        positions = [0, 0, 0, size, 0, 0,
                     0, 0, 0, 0, size, 0,
                     0, 0, 0, 0, 0, size]
        colors = [1.0, 0.0, 0.0, 1.0,  1.0, 0.0, 0.0, 1.0,
                  0.0, 1.0, 0.0, 1.0,  0.0, 1.0, 0.0, 1.0,
                  0.0, 0.0, 1.0, 1.0,  0.0, 0.0, 1.0, 1.0]
        from imptux.renderer import VertexGeometry
        self.vertex_geom = VertexGeometry(renderer.ctx, positions, colors)
        self.x = x
        self.y = y
        self.z = z

    def draw(self):
        renderer.matrix_stack.push()
        renderer.matrix_stack.translate(self.x, self.y, self.z)
        renderer.set_color(1.0, 1.0, 1.0)
        renderer.draw(self.vertex_geom)
        renderer.matrix_stack.pop()


class Border(object):
    def __init__(self, width, height, color=(1., 1., 1.)):
        self.color = color
        points = [0, 0, 0, 0, height, 0,
                  0, height, 0, width, height, 0,
                  width, height, 0, width, 0, 0,
                  width, 0, 0, 0, 0, 0]
        for n in range(len(points) // 3):
            points[n * 3] += width / -2
            points[n * 3 + 1] += height / -2
        from imptux.renderer import VertexGeometry
        self.vertex_geom = VertexGeometry(renderer.ctx, points)

    def draw(self):
        renderer.set_color(*self.color)
        renderer.draw(self.vertex_geom)
