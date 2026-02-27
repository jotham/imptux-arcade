"""Modern OpenGL rendering helpers for Arcade 3.x (replaces Pyglet 1.1 fixed-function pipeline)."""

import math
import struct
from pyglet.math import Mat4, Vec3
from arcade.gl import BufferDescription

VERTEX_SHADER = """
#version 330 core
in vec3 in_position;
in vec4 in_color;
uniform mat4 mvp;
uniform vec4 u_color;
out vec4 v_color;
void main() {
    gl_Position = mvp * vec4(in_position, 1.0);
    v_color = in_color * u_color;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec4 v_color;
out vec4 fragColor;
void main() { fragColor = v_color; }
"""


class VertexGeometry:
    """Holds GPU buffers for a set of 3D line vertices (replaces pyglet.graphics.vertex_list)."""

    def __init__(self, ctx, positions, colors=None):
        """
        positions: flat float list of XYZ triples
        colors: optional flat float list of RGBA values; defaults to all white
        """
        self.ctx = ctx
        n = len(positions) // 3
        self._n = n
        if colors is None:
            colors = [1.0, 1.0, 1.0, 1.0] * n

        pos_data = struct.pack(f'{len(positions)}f', *positions)
        col_data = struct.pack(f'{len(colors)}f', *colors)

        self._vbo_pos = ctx.buffer(data=pos_data)
        self._vbo_col = ctx.buffer(data=col_data)

        self._geometry = ctx.geometry(
            [
                BufferDescription(self._vbo_pos, '3f', ['in_position']),
                BufferDescription(self._vbo_col, '4f', ['in_color']),
            ],
        )

    def render(self, program, mode):
        self._geometry.render(program, mode=mode, vertices=self._n)


class MatrixStack:
    """Minimal matrix stack (replaces glPushMatrix/glPopMatrix/glTranslatef/glRotatef)."""

    def __init__(self):
        self._stack = [Mat4()]  # identity

    def push(self):
        self._stack.append(Mat4(*self._stack[-1]))

    def pop(self):
        if len(self._stack) > 1:
            self._stack.pop()

    def load_identity(self):
        self._stack[-1] = Mat4()

    def translate(self, x, y, z):
        t = Mat4.from_translation(Vec3(x, y, z))
        self._stack[-1] = self._stack[-1] @ t

    def rotate(self, angle_deg, x, y, z):
        # Normalise axis
        length = math.sqrt(x*x + y*y + z*z)
        if length == 0:
            return
        x, y, z = x/length, y/length, z/length
        angle_rad = math.radians(angle_deg)
        r = Mat4.from_rotation(angle_rad, Vec3(x, y, z))
        self._stack[-1] = self._stack[-1] @ r

    def current(self):
        return self._stack[-1]


class Renderer:
    """Singleton renderer — initialised once after the Arcade window is created."""

    def __init__(self):
        self.ctx = None
        self._program = None
        self.projection = Mat4()
        self.matrix_stack = MatrixStack()
        self._color = (1.0, 1.0, 1.0, 1.0)

    def init(self, ctx):
        self.ctx = ctx
        self._program = ctx.program(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER,
        )

    def set_color(self, r, g, b, a=1.0):
        self._color = (r, g, b, a)

    def draw(self, geometry):
        mvp = self.projection @ self.matrix_stack.current()
        self._program['mvp'] = mvp
        self._program['u_color'] = self._color
        geometry.render(self._program, self.ctx.LINES)

    def enable_depth_test(self):
        self.ctx.enable(self.ctx.DEPTH_TEST)

    def disable_depth_test(self):
        self.ctx.disable(self.ctx.DEPTH_TEST)


# Global singleton — call renderer.init(ctx) once after window creation
renderer = Renderer()
