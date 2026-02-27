#!/usr/bin/env python3

import imptux, time, math, random, os
import imptux.models
import arcade
from pyglet import gl

# generate displacement map for terrain cage
displacement_resolution = 1024
displacement_resolution_ = displacement_resolution - 1
displacement_map = []
for n in range(displacement_resolution):
    angle = math.pi * 1.33 + n/float(displacement_resolution) * math.pi/2.9
    displacement_map.append(((angle-math.pi/2)*180/math.pi, 600*math.cos(angle), 600*math.sin(angle)+358))
def get_displacement (n):
    set = int(((n + 220) / 440.0)*displacement_resolution_)
    return displacement_map[set][0], displacement_map[set][1], displacement_map[set][2]

def prepare (xo,yo,zo,xs,ys,zs,v):
    return_list = []
    for n in range(int(len(v)/3)):
        return_list.extend([xo+v[n*3]*xs,yo+v[n*3+1]*ys,zo+v[n*3+2]*zs])
    return return_list
  
def make_debris (count):
    spreadx = 50
    spreadz = 25
    offsetz = 35
    length = 25
    return_list = []
    for n in range(count):
        lines = []
        for line in range(5):
            x = spreadx*(random.random()-0.5)
            y = 0
            z = offsetz+spreadz*(random.random()-0.5)
            len = random.randrange(length)+2
            lines.extend([x,y,z,x,y,z+len])
        return_list.append(pyglet.graphics.vertex_list(10,('v3f/static', lines)))
    return return_list

# SND_PEW = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','pew 1.ogg')))
# SND_SHIELD = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','shield.ogg')))
# SND_GRIND1 = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','grind 1.ogg')))
# SND_GRIND2 = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','grind 2.ogg')))
# SND_ZUB1 = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','zub 1.ogg')))
# SND_PEW3 = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','pew 3.ogg')))
# SND_DHHHD = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','dhhhd.ogg')))
# SND_ENTRANCE = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','entrance.ogg')))
# SND_GAME_MUSIC = pyglet.media.StaticSource(pyglet.media.load(os.path.join(os.getcwd(), 'assets','imptux-1.ogg')))

PLAYER_VERTEX_LIST = (-50.0, 10.000002, 0.0, 50.0, 10.000002, 0.0, 50.0, 10.000002, 0.0, 50.0, -9.999998, 0.0, 50.0, -9.999998, 0.0, -50.0, -9.999998, 0.0, -50.0, -9.999998, 0.0, -50.0, 10.000002, 0.0, 50.0, -9.999998, 0.0, 50.0, 10.000002, 0.0, 50.0, 10.000002, 0.0, 0.0, -2e-06, -100.0, 0.0, -2e-06, -100.0, 50.0, -9.999998, 0.0, 50.0, 10.000002, 0.0, -50.0, 10.000002, 0.0, -50.0, 10.000002, 0.0, 0.0, -2e-06, -100.0, 0.0, -2e-06, -100.0, 50.0, 10.000002, 0.0, -50.0, 10.000002, 0.0, -50.0, -9.999998, 0.0, -50.0, -9.999998, 0.0, 0.0, -2e-06, -100.0, 0.0, -2e-06, -100.0, -50.0, 10.000002, 0.0, -50.0, -9.999998, 0.0, 50.0, -9.999998, 0.0, 50.0, -9.999998, 0.0, 0.0, -2e-06, -100.0, 0.0, -2e-06, -100.0, -50.0, -9.999998, 0.0)
TERRAIN_VERTEX_LIST = (-400, 30, -2000, -330, 30, -2000, -330, 30, -2000, -330, 30, 0, -330, 30, 0, -400, 30, 0, -400, 30, 0, -400, 30, -2000, -330, 30, -2000, -324.956177, 29.579521, -2000, -324.956177, 29.579521, -2000, -324.956177, 29.579521, 0, -324.956177, 29.579521, 0, -330, 30, 0, -330, 30, 0, -330, 30, -2000, -324.956177, 29.579521, -2000, -319.409271, 28.364159, -2000, -319.409271, 28.364159, -2000, -319.409271, 28.364159, 0, -319.409271, 28.364159, 0, -324.956177, 29.579521, 0, -324.956177, 29.579521, 0, -324.956177, 29.579521, -2000, -319.409271, 28.364159, -2000, -310.095367, 25.20192, -2000, -310.095367, 25.20192, -2000, -310.095367, 25.20192, 0, -310.095367, 25.20192, 0, -319.409271, 28.364159, 0, -319.409271, 28.364159, 0, -319.409271, 28.364159, -2000, -310.095367, 25.20192, -2000, -283.322876, 12.78336, -2000, -283.322876, 12.78336, -2000, -283.322876, 12.78336, 0, -283.322876, 12.78336, 0, -310.095367, 25.20192, 0, -310.095367, 25.20192, 0, -310.095367, 25.20192, -2000, -283.322876, 12.78336, -2000, -205.223038, -23.061121, -2000, -205.223038, -23.061121, -2000, -205.223038, -23.061121, 0, -205.223038, -23.061121, 0, -283.322876, 12.78336, 0, -283.322876, 12.78336, 0, -283.322876, 12.78336, -2000, -205.223038, -23.061121, -2000, -160.174072, -38.25024, -2000, -160.174072, -38.25024, -2000, -160.174072, -38.25024, 0, -160.174072, -38.25024, 0, -205.223038, -23.061121, 0, -205.223038, -23.061121, 0, -205.223038, -23.061121, -2000, -160.174072, -38.25024, -2000, -107.280006, -50.640003, -2000, -107.280006, -50.640003, -2000, -107.280006, -50.640003, 0, -107.280006, -50.640003, 0, -160.174072, -38.25024, 0, -160.174072, -38.25024, 0, -160.174072, -38.25024, -2000, -107.280006, -50.640003, -2000, -56.760002, -57.48, -2000, -56.760002, -57.48, -2000, -56.760002, -57.48, 0, -56.760002, -57.48, 0, -107.280006, -50.640003, 0, -107.280006, -50.640003, 0, -107.280006, -50.640003, -2000, -56.760002, -57.48, -2000, 0, -60, -2000, 0, -60, -2000, 0, -60, 0, 0, -60, 0, -56.760002, -57.48, 0, -56.760002, -57.48, 0, -56.760002, -57.48, -2000, 0, -60, -2000, 56.400002, -57.48, -2000, 56.400002, -57.48, -2000, 56.400002, -57.48, 0, 56.400002, -57.48, 0, 0, -60, 0, 0, -60, 0, 0, -60, -2000, 56.400002, -57.48, -2000, 106.000008, -50.640003, -2000, 106.000008, -50.640003, -2000, 106.000008, -50.640003, 0, 106.000008, -50.640003, 0, 56.400002, -57.48, 0, 56.400002, -57.48, 0, 56.400002, -57.48, -2000, 106.000008, -50.640003, -2000, 149.400009, -40.559998, -2000, 149.400009, -40.559998, -2000, 149.400009, -40.559998, 0, 149.400009, -40.559998, 0, 106.000008, -50.640003, 0, 106.000008, -50.640003, 0, 106.000008, -50.640003, -2000, 149.400009, -40.559998, -2000, 194.140793, -25.70784, -2000, 194.140793, -25.70784, -2000, 194.140793, -25.70784, 0, 194.140793, -25.70784, 0, 149.400009, -40.559998, 0, 149.400009, -40.559998, 0, 149.400009, -40.559998, -2000, 194.140793, -25.70784, -2000, 248.400009, -1.68, -2000, 248.400009, -1.68, -2000, 248.400009, -1.68, 0, 248.400009, -1.68, 0, 194.140793, -25.70784, 0, 194.140793, -25.70784, 0, 194.140793, -25.70784, -2000, 248.400009, -1.68, -2000, 302.198395, 23.825281, -2000, 302.198395, 23.825281, -2000, 302.198395, 23.825281, 0, 302.198395, 23.825281, 0, 248.400009, -1.68, 0, 248.400009, -1.68, 0, 248.400009, -1.68, -2000, 302.198395, 23.825281, -2000, 313.200012, 27.48, -2000, 313.200012, 27.48, -2000, 313.200012, 27.48, 0, 313.200012, 27.48, 0, 302.198395, 23.825281, 0, 302.198395, 23.825281, 0, 302.198395, 23.825281, -2000, 313.200012, 27.48, -2000, 320.126404, 29.066881, -2000, 320.126404, 29.066881, -2000, 320.126404, 29.066881, 0, 320.126404, 29.066881, 0, 313.200012, 27.48, 0, 313.200012, 27.48, 0, 313.200012, 27.48, -2000, 320.126404, 29.066881, -2000, 323.481598, 29.579521, -2000, 323.481598, 29.579521, -2000, 323.481598, 29.579521, 0, 323.481598, 29.579521, 0, 320.126404, 29.066881, 0, 320.126404, 29.066881, 0, 320.126404, 29.066881, -2000, 323.481598, 29.579521, -2000, 330, 30, -2000, 330, 30, -2000, 330, 30, 0, 330, 30, 0, 323.481598, 29.579521, 0, 323.481598, 29.579521, 0, 323.481598, 29.579521, -2000, 330, 30, -2000, 400, 30, -2000, 400, 30, -2000, 400, 30, 0, 400, 30, 0, 330, 30, 0, 330, 30, 0, 330, 30, -2000)
TERRAIN_VERTEX_LIST_2 = prepare(0,0,500,2,2,4,imptux.models.MODEL_CAGE)
ENEMY_VERTEX_LIST = (-50.0, 10.000002, -100.0, 50.0, 10.000002, -100.0, 50.0, 10.000002, -100.0, 50.0, -9.999998, -100.0, 50.0, -9.999998, -100.0, -50.0, -9.999998, -100.0, -50.0, -9.999998, -100.0, -50.0, 10.000002, -100.0, 50.0, -9.999998, -100.0, 50.0, 10.000002, -100.0, 50.0, 10.000002, -100.0, 0.0, -2e-06, 0.0, 0.0, -2e-06, 0.0, 50.0, -9.999998, -100.0, 50.0, 10.000002, -100.0, -50.0, 10.000002, -100.0, -50.0, 10.000002, -100.0, 0.0, -2e-06, 0.0, 0.0, -2e-06, 0.0, 50.0, 10.000002, -100.0, -50.0, 10.000002, -100.0, -50.0, -9.999998, -100.0, -50.0, -9.999998, -100.0, 0.0, -2e-06, 0.0, 0.0, -2e-06, 0.0, -50.0, 10.000002, -100.0, -50.0, -9.999998, -100.0, 50.0, -9.999998, -100.0, 50.0, -9.999998, -100.0, 0.0, -2e-06, 0.0, 0.0, -2e-06, 0.0, -50.0, -9.999998, -100.0)
PLAYER_BULLET_VERTEX_LIST = (-10, 0, 5, 0, 0, -5, 0, 0, -5, 10, 0, 5, 10, 0, 5, -10, 0, 5)
PILLAR_PAIR = prepare(-300,30,0,1,1,1,imptux.models.MODEL_PILLAR)
PILLAR_PAIR.extend(prepare(300,30,0,-1,1,1,imptux.models.MODEL_PILLAR))
PLAYER_SHIP_2 = prepare(0,0,0,0.25,-0.25,-0.25,imptux.models.MODEL_SHIP)
PLAYER_SHIELD = prepare(0,0,0,0.25,-0.25,-0.25,imptux.models.MODEL_PLAYER_SHIELD)
PAYLOAD_SHIP = prepare(0,-100,0,1,-1,1,imptux.models.MODEL_PAYLOAD)
PAYLOAD_SHIP_2 = prepare(0,-100,0,1,-1,1,imptux.models.MODEL_PAYLOAD_2)
#~ ENCRYPTER_SHIP_2 = prepare(0,0,0,0.25,.5,0.25,imptux.models.MODEL_ENCRYPTER_2)
PAYLOAD_MUNITION = prepare(0,0,0,0.5,0.5,0.5,imptux.models.MODEL_PAYLOAD_MUNITION)
PAYLOAD_SHIELD = prepare(0,-100,0,1,1,1,imptux.models.MODEL_PAYLOAD_SHIELD)

DEBUG = False

ENCRYPTER_MUNITION_STRENGTH = 8
ENCRYPTER_HEALTH = 1

PAYLOAD_MUNITION_STRENGTH = 15
PAYLOAD_HEALTH = 50

PLAYER_HEALTH = 100

class Terrain (object):
    model = pyglet.graphics.vertex_list(168,('v3f/static', prepare(0,0,0,1,1,4,TERRAIN_VERTEX_LIST)))
    #~ model = pyglet.graphics.vertex_list(320,('v3f/static', TERRAIN_VERTEX_LIST_2))
    
    def __init__ (self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        pillar_count = 8
        spacing = 800
        self.pillars = [TerrainPillarPair(0,-200,n*-spacing, -spacing*pillar_count) for n in range(pillar_count)]
        
    def update (self, dt):
        for pillar in self.pillars:
            pillar.update(dt)
        return True
    
    def draw (self):
        gl.glColor3f(0.38, 0, 0)
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, self.z)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()
        for pillar in self.pillars:
            pillar.draw()

class TerrainPillarPair (object):
    model = pyglet.graphics.vertex_list(312*2,('v3f/static', PILLAR_PAIR))
    
    def __init__ (self, x, y, z, boundsz):
        self.x = x
        self.y = y
        self.z = z
        self.vz = 2000
        self.boundsz = boundsz
        self.hidden = random.random() < 0.5
        
    def update (self, dt):
        self.z += self.vz * dt
        if self.z >= 0:
            self.z = self.boundsz+self.z
            self.hidden = random.random() < 0.5
        return True
    
    def draw (self):
        if self.hidden: return
        gl.glColor3f(0.38, 0, 0)
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, self.z)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()

class PlayerBulletModel (object):
    model = pyglet.graphics.vertex_list(6, ('v3f/static', prepare(0,0,0,0.5,0.5,0.5,PLAYER_BULLET_VERTEX_LIST)))
    
    def __init__ (self, x, y, z, vx=0, vz=-650):
        self.x = x
        self.y = y
        self.z = z
        self.rz = 0
        self.vrz = 0
        self.vz = vz
        self.vx = vx
        self.boundsz = -2000
        self.active = True
        self.update()
        
    def update (self, dt=0):
        if not self.active or self.z < self.boundsz or self.x < -200 or self.x > 200:
            return False
        self.z += self.vz * dt
        self.x += self.vx * dt
        self.left = self.x - 5#10
        self.right = self.x + 5#10
        self.top = self.z + 2.5#5
        self.bottom = self.z - 2.5#5
        self.rz += self.vrz * dt
        self.virtual_rz, self.virtual_x, self.virtual_y = get_displacement(self.x)
        return True
    
    def collision (self, entity):
        self.active = False
        
    def draw (self):
        gl.glColor3f(1, 0.8, 0)
        gl.glPushMatrix()
        gl.glTranslatef(self.virtual_x, self.virtual_y, self.z)
        gl.glRotatef(self.virtual_rz+self.rz,0,0,1)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()

class PlayerBulletModelSpecial (object):
    # TODO: FIX BOUNDING BOX FOR THIS MUNITION
    model = pyglet.graphics.vertex_list(6, ('v3f/static', prepare(0,0,0,0.5,0.5,5,PLAYER_BULLET_VERTEX_LIST)))
    
    def __init__ (self, x, y, z, vx=0, vz=-650):
        self.x = x
        self.y = y
        self.z = z
        self.rz = 0
        self.vrz = 500
        if x < 0:
            self.vrz *= -1
        self.vz = vz
        self.vx = vx
        self.boundsz = -2000
        self.active = True
        self.update()
        
    def update (self, dt=0):
        if not self.active or self.z < self.boundsz or self.x < -200 or self.x > 200:
            return False
        self.z += self.vz * dt
        self.x += self.vx * dt
        self.left = self.x - 5#10
        self.right = self.x + 5#10
        self.top = self.z + 2.5#5
        self.bottom = self.z - 2.5#5
        self.rz += self.vrz * dt
        self.virtual_rz, self.virtual_x, self.virtual_y = get_displacement(self.x)
        return True
    
    def collision (self, entity):
        self.active = False
        
    def draw (self):
        b = random.random()*0.6
        gl.glColor3f(b, b, 1.0)
        gl.glPushMatrix()
        gl.glTranslatef(self.virtual_x, self.virtual_y, self.z)
        gl.glRotatef(self.virtual_rz+self.rz,0,0,1)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()
      
class Player (object):
    #~ model = pyglet.graphics.vertex_list(32,('v3f/static', prepare(0,0,0,0.5,0.5,0.5, PLAYER_VERTEX_LIST)))
    model = pyglet.graphics.vertex_list(164,('v3f/static', PLAYER_SHIP_2))
    shield = pyglet.graphics.vertex_list(120,('v3f/static', PLAYER_SHIELD))
    debris = make_debris(5)
    
    # sound_player = pyglet.media.Player()
    
    def __init__ (self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.yoffset = 0
        self.decay = 1
        self.iv = 450
        self.fire_delay = .125
        self.timestamp_a = 0
        self.timestamp_b = 0
        self.heal_timestamp = 0
        self.weapon_a_cooldown = 0
        self.weapon_b_cooldown = 0
        self.heal_rate = 0.33
        self.health = PLAYER_HEALTH
        self.maximum_health = PLAYER_HEALTH
        self.c = 0
        self.boundsx = 200
        self.bounce_rate = 9
        self.bounce = 0
        self.new_grind = True
        self.update()
        
    def draw (self):
        gl.glPushMatrix()
        gl.glTranslatef(self.virtual_x, self.virtual_y+self.yoffset, self.z)
        gl.glRotatef(self.virtual_rz,0,0,1)
        
        if self.x < -180 or self.x > 180:
            # random lines
            c = random.random()
            gl.glColor3f(1.0*c, 1.0 *c, 0)
            random.choice(self.debris).draw(gl.GL_LINES)
            if self.new_grind:
                self.new_grind = False
                # SND_GRIND2.play()
                #~ self.sound_player.queue(SND_GRIND2)
                #~ self.sound_player.next()
                #~ self.sound_player.play()
                # queue sound
        else:
            self.new_grind = True
        
        if self.c > 0.5:
            c2 = self.c/2.0
            gl.glColor3f(c2*0.5,c2*0.5, c2*2)
            self.shield.draw(gl.GL_LINES)
        gl.glColor3f(0.2+.8*self.c, 0.7+-.5*self.c, 0)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()
    
    def update (self, dt=0, now=0):
        self.x = max(-self.boundsx, min(self.boundsx, self.x + (self.vx * dt) ))
        self.left = self.x - 28
        self.right = self.x + 28
        self.top = self.z + 23
        self.bottom = self.z - 23
        self.c *= .8
        self.vx *= self.decay
        self.yoffset = 4*math.sin(self.bounce)
        self.bounce += self.bounce_rate * dt
        self.virtual_rz, self.virtual_x, self.virtual_y = get_displacement(self.x)
        if self.heal_timestamp < now and self.health < self.maximum_health:
            self.heal_timestamp = now + self.heal_rate
            self.health += 1
        return True
        
    def move_left (self, mode):
        if mode == 1:
            self.decay = 1
            self.vx = -self.iv
        elif self.vx < 0:
            self.decay = 0.5
            
    def move_right (self, mode):
        if mode == 1:
            self.decay = 1
            self.vx = self.iv
        elif self.vx > 0:
            self.decay = 0.5
    
    def move_free (self, amount):
        if abs(amount) < 0.2:
            self.decay = 0.5
        else:
            self.decay = 1
            self.vx = amount * self.iv
            
    def fire (self, now, mode=0):
        if mode == 0 and now > self.timestamp_a:
            self.timestamp_a = now + 0.1 + (self.weapon_a_cooldown/100.0)
            # SND_PEW.play()
            return (PlayerBulletModel(self.x-12, self.y, self.z+5, 5),PlayerBulletModel(self.x+12, self.y, self.z+5, -5))
        elif mode == 1 and now > self.timestamp_b:
            self.timestamp_b = now + 0.15 + (self.weapon_b_cooldown/100.0)
            # SND_PEW3.play()
            return (
                PlayerBulletModelSpecial(self.x-25, self.y, self.z+15, 5),
                PlayerBulletModelSpecial(self.x+25, self.y, self.z+15, -5))
        return None
    
    def collision_entity (self, entity):
        SND_SHIELD.play()
        self.health -= 15
        self.c = 1
        
    def collision_entity_munition (self, entity_munition):
        SND_SHIELD.play()
        self.health -= entity_munition.strength
        self.c = 1.5

class EncrypterDrone (object):
    model = pyglet.graphics.vertex_list(32,('v3f/static', prepare(0,0,0,0.5,0.5,0.5,ENEMY_VERTEX_LIST)))
    #~ model = pyglet.graphics.vertex_list(208,('v3f/static', ENCRYPTER_SHIP_2))
    
    def __init__ (self, x, y, z, vz, phase_offset, phase_rate, phase_amplitude, appear_delay, fire_cycle, dispatch_callback):
        self.x = x
        self.y = y
        self.z = z
        self.vz = vz
        self.health = ENCRYPTER_HEALTH
        self.phase = phase_offset
        self.phase_rate = phase_rate
        self.phase_amplitude = phase_amplitude
        self.active = False
        self.active_timestamp = appear_delay
        self.fire_cycle = fire_cycle
        self.fire_timestamp = 0
        self.dispatch_callback = dispatch_callback
        self.c = 0
        self.update()
        
    def update (self, dt=0, now=0):
        if self.health < 0 or self.z > 0:
            return False
        self.phase += self.phase_rate * dt
        self.x = self.phase_amplitude * math.sin(self.phase)
        self.z += self.vz * dt
        self.left = self.x - 25
        self.right = self.x + 25
        self.top = self.z + 0
        self.bottom = self.z - 50
        self.c *= .9
        if self.active and self.fire_cycle and self.fire_timestamp < now:
            self.dispatch_callback([EncryptionMunition(self.x, self.y, self.z+20)])
            self.fire_timestamp = now + self.fire_cycle
        self.virtual_rz, self.virtual_x, self.virtual_y = get_displacement(self.x)
        if not self.active:
            if self.active_timestamp < now:
                self.active = True
                self.fire_timestamp = now + self.fire_cycle
        return True
    
    def draw (self):
        if not self.active:
            return
        gl.glPushMatrix()
        gl.glTranslatef(self.virtual_x, self.virtual_y, self.z)
        gl.glRotatef(self.virtual_rz,0,0,1)
        gl.glColor3f(1.0, self.c, 0)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()
        
    def collision (self, munition):
        self.c = 1
        self.health -= 1
        
    def collision_player (self, player):
        self.health = 0
        
class EncryptionMunition (object):
    model = pyglet.graphics.vertex_list(6, ('v3f/static', prepare(0,0,0,0.55,0.55,-0.5,PLAYER_BULLET_VERTEX_LIST)))
    #~ model = pyglet.graphics.vertex_list(64,('v3f/static', PAYLOAD_MUNITION))
    
    def __init__ (self, x, y, z, vx=0, vz=1100):
        self.x = x
        self.y = y
        self.z = z
        self.rz = 0
        self.vrz = -500
        self.vz = vz
        self.vx = vx
        self.strength = ENCRYPTER_MUNITION_STRENGTH
        self.boundsz = 0
        self.active = True
        self.update()
        
    def update (self, dt=0, now=0):
        if (not self.active) or self.z > self.boundsz or self.x < -200 or self.x > 200:
            return False
        self.z += self.vz * dt
        self.x += self.vx * dt
        self.left = self.x - 5#10
        self.right = self.x + 5#10
        self.top = self.z + 0 #5
        self.bottom = self.z - 2.5#5
        self.virtual_rz, self.virtual_x, self.virtual_y = get_displacement(self.x)
        return True
    
    def collision (self, entity):
        self.active = False
        
    def collision_player (self, player):
        self.active = False
        
    def draw (self):
        b = random.random()*0.6
        gl.glColor3f(b, b, 1.0)
        gl.glPushMatrix()
        gl.glTranslatef(self.virtual_x, self.virtual_y, self.z)
        gl.glRotatef(self.virtual_rz+self.rz,0,0,1)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()
        
class PayloadMunition (object):
    #~ model = pyglet.graphics.vertex_list(6, ('v3f/static', prepare(0,0,0,0.25,0.25,-0.5,PLAYER_BULLET_VERTEX_LIST)))
    model = pyglet.graphics.vertex_list(64,('v3f/static', PAYLOAD_MUNITION))
    
    def __init__ (self, x, y, z, vx=0, vz=1100):
        self.x = x
        self.y = y
        self.z = z
        self.rz = 0
        self.vrz = -500
        self.vz = vz
        self.vx = vx
        self.strength = PAYLOAD_MUNITION_STRENGTH
        self.boundsz = 0
        self.active = True
        SND_DHHHD.play()
        self.update()
        
    def update (self, dt=0, now=0):
        if not self.active or self.z > self.boundsz or self.x < -200 or self.x > 200:
            return False
        self.z += self.vz * dt
        self.x += self.vx * dt
        self.left = self.x - 5#10
        self.right = self.x + 5#10
        self.top = self.z + 0 #5
        self.bottom = self.z - 2.5#5
        self.virtual_rz, self.virtual_x, self.virtual_y = get_displacement(self.x)
        return True
    
    def collision (self, entity):
        self.active = False
        
    def collision_player (self, player):
        self.active = False
        
    def draw (self):
        b = random.random()*0.6
        gl.glColor3f(b, b, 1.0)
        gl.glPushMatrix()
        gl.glTranslatef(self.virtual_x, self.virtual_y, self.z)
        gl.glRotatef(self.virtual_rz+self.rz,0,0,1)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()
        
class PayloadDrone (object):
    #~ model = pyglet.graphics.vertex_list(360,('v3f/static', PAYLOAD_SHIP))
    model = pyglet.graphics.vertex_list(496,('v3f/static', PAYLOAD_SHIP_2))
    shield = pyglet.graphics.vertex_list(120,('v3f/static', PAYLOAD_SHIELD))
    
    def __init__ (self, x, y, z, phase, appear_delay, fire_cycle, dispatch_callback):
        self.x = x
        self.y = y
        self.z = z
        self.vz = 4070
        self.yoffset = 0
        self.health = PAYLOAD_HEALTH
        self.bounce_rate = 4
        self.bounce = 0
        #~ self.step = 0
        #~ self.step_rate = math.pi/2
        self.phase = phase
        self.active = False
        self.step = 0
        self.active_timestamp = time.time()
        self.appear_delay = appear_delay
        self.fire_delay = 0.3
        self.dispatch_callback = dispatch_callback
        self.c = 0
        SND_ENTRANCE.play()
        self.update()
        
    def update (self, dt=0, now=0):
        if self.health < 0 or self.z > 0:
            self.health = 0
            return False
        #~ self.step += self.step_rate * dt
        #~ self.x = 200 * math.sin(self.step+self.phase)
        if self.z < -1800:
            self.z += self.vz * dt
            self.fire_timestamp = now
        
        if self.fire_timestamp < now:
            self.fire_timestamp = now + self.fire_delay
            xoff = (self.step/4.0) * 100 - 50
            #~ SND_ZUB1.volume = 0.2
            #~ SND_ZUB1.play()
            self.dispatch_callback([PayloadMunition(self.x+xoff, self.y, self.z+150, xoff)])
            self.step += 1
            if self.step > 6:
                self.step = 0
                if self.fire_delay > 0.2:
                    self.fire_delay *= 0.95
            
        self.yoffset = 4*math.sin(self.bounce)
        self.bounce += self.bounce_rate * dt
            
        self.left = self.x - 80
        self.right = self.x + 80
        self.top = self.z + 139
        self.bottom = self.z - 115
        self.c *= .9
        self.virtual_rz, self.virtual_x, self.virtual_y = get_displacement(self.x)
        #~ if not self.active:
            #~ if self.active_timestamp < now:
                #~ self.active = True
        return True
    
    def draw (self):
        #~ if not self.active:
            #~ return
            
        #~ gl.glColor3f(1.0, 0, 1.0)
        #~ pyglet.graphics.vertex_list(8, ('v3f/static', (
            #~ self.left, self.y, self.bottom, self.left, self.y, self.top, self.left, self.y,
            #~ self.top, self.right, self.y, self.top, self.right, self.y, self.top, self.right, self.y,
            #~ self.bottom, self.right, self.y, self.bottom, self.left, self.y, self.bottom))).draw(gl.GL_LINES)

        gl.glPushMatrix()
        gl.glTranslatef(self.virtual_x, self.virtual_y+self.yoffset, self.z+self.yoffset*5)
        gl.glRotatef(self.virtual_rz,0,0,1)
                    
        if self.c > 0.5:
            c2 = self.c/2.0
            gl.glColor3f(c2*.5,c2*0.1, c2*0.1)
            self.shield.draw(gl.GL_LINES)
            
        gl.glColor3f(0.8+0.2*self.c, 0.1, 0.9*self.c)
        self.model.draw(gl.GL_LINES)
        gl.glPopMatrix()
        
    def collision (self, munition):
        if self.z < -1800: return
        self.c = 1
        self.health -= 1
        
    def collision_player (self, player):
        self.health = 0

def make_fire_probability (probability, sizes=(1, 4, 0.2)):
    if random.random() < probability:
        return random.choice(sizes)
    return 0
    
class LevelOne (object):
    label = 'LEVEL: TRAFFIC'
    
    def __init__ (self, dispatch_callback, dispatch_b_callback, dispatch_entity_munitions_callback):
        #~ super(EventDispatcher, self).__init__()
        self.dispatch_callback = dispatch_callback
        self.dispatch_b_callback = dispatch_b_callback
        self.dispatch_entity_munitions_callback = dispatch_entity_munitions_callback
        self.drone_timestamp = time.time() 
        self.drone_period = 2
        self.start_timestamp = self.drone_timestamp + 3
        self.wave_counter = 0
        self.mode = 0
        self.payload = None
    
    def update (self, dt):
        now = time.time()
        if self.drone_timestamp > now or self.start_timestamp > now:
            return
        if self.payload and self.payload.health <= 0:
            self.payload = None
        self.drone_timestamp = now + self.drone_period
        if self.mode == 0:
            count = 6.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-50, 600, n/count*-math.pi/2, math.pi/4, 200, now+n*.35, make_fire_probability(0.2), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2465 + n*-50, 600,(n/count*-math.pi/2)+math.pi, math.pi/4, 200, now+n*.35, make_fire_probability(0.2), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.wave_counter += 1
            if self.wave_counter > 6:
                self.mode = 1
                self.wave_counter = 0
                print(self.mode)
        elif self.mode == 1:
            count = 3.0 
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-60, 600, n/count*-math.pi/2, math.pi/2, 200, 1+now+n*.35, 1.5*(n+1)/count, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2600 + n*-60, 600, n/count*-math.pi/2, math.pi/2, 50, now+n*.35, (1.5+(n+1)/count)*2, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2765 + n*-60, 600, n/count*-math.pi/2, math.pi/2, -50, now+n*.35, (1.5+(n+1)/count)*2, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2165 + n*-60, 600, (n/count*-math.pi/2)+math.pi, math.pi/2, 200, 1+now+n*.35, 1.5*(n+1)/count, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_entity_munitions_callback([EncryptionMunition(50*(n/6.0 - 0.5), -200, -2000, 50*(n/6.0 - 0.5)) for n in range(6)])
            self.wave_counter += 1
            if self.wave_counter > 6:
                self.mode = 2
                self.wave_counter = 0
                print(self.mode)
        elif self.mode == 2:
            count = 6.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-110, 600, n/count*-math.pi/2, math.pi/2, 200, now+n*.35, make_fire_probability(0.1, (0.25,1.0)), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2465 + n*-110, 600, (n/count*-math.pi/2)+math.pi, math.pi/2, 200, now+n*.35, make_fire_probability(0.1, (0.25,1.0)), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.wave_counter += 1
            if self.wave_counter > 6:
                self.mode = 3
                self.wave_counter = 0
                print(self.mode)
        elif self.mode == 3:
            count = 4.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-110, 600, n/count*-math.pi/2, math.pi/2, 200, now+n*.35, 0, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2465 + n*-110, 600, (n/count*-math.pi/2)+math.pi, math.pi/2, 200, now+n*.35, 0, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.payload = PayloadDrone(0, -200, -8000, 0, 0, 1, self.dispatch_entity_munitions_callback)
            self.wave_counter += 1
            self.dispatch_b_callback([self.payload])
            self.mode = 4
        elif self.mode == 4:
            count = 2.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-110, 600, n/count*-math.pi/2, math.pi/2, 200, now+n*.35, 0, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2465 + n*-110, 600, (n/count*-math.pi/2)+math.pi, math.pi/2, 200, now+n*.35, 0, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.wave_counter += 1
            if not self.payload and self.wave_counter > 18:
                self.mode = 5
                self.wave_counter = 0
                print(self.mode)
        elif self.mode == 5:
            count = 4.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-110, 600, n/count*-math.pi/2, math.pi/2, 200, now+n*.35, make_fire_probability(0.09, (0.09,1.0,0.1)), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2465 + n*-110, 600, (n/count*-math.pi/2)+math.pi, math.pi/2, 200, now+n*.35, make_fire_probability(0.09, (0.25,1.0,0.1)), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_entity_munitions_callback([EncryptionMunition(20*(n/6.0 - 0.5), -200, -2000, 70*(n/6.0 - 0.5)) for n in range(6)])
            if random.random() < 0.2:
                self.dispatch_entity_munitions_callback([PayloadMunition(400*(n/5.0 - 0.5), -200, -2000+random.random()*500, 100*(n/6.0 - 0.5)) for n in range(5)])
            self.wave_counter += 1
            if self.wave_counter > 8:
                self.mode = 6
                self.wave_counter = 0
                print(self.mode)
        elif self.mode == 6:
            #~ x, y, z, phase_offset, phase_rate, phase_amplitude, appear_delay, fire_cycle, dispatch_callback
            count = 8.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-110, 600, n/count*-math.pi/4.0, math.pi/8.0, 100, now+n*0.2, 0, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            count = 3.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2300 + n*-110, 700, n/count*-math.pi/4.0, math.pi/2.0, -190, now+n*0.2, 0.5+(n/count*0.5), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_entity_munitions_callback([EncryptionMunition(20*(n/6.0 - 0.5), -200, -2500+(n*100), 48+random.randrange(5)) for n in range(6)])
            self.wave_counter += 1
            if self.wave_counter > 4:
                self.mode = 7
                self.wave_counter = 0
                print(self.mode)
        elif self.mode == 7:
            #~ x, y, z, phase_offset, phase_rate, phase_amplitude, appear_delay, fire_cycle, dispatch_callback
            count = 8.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2400 + n*-110, 600, n/count*-math.pi/4.0, math.pi/8.0, -100, now+n*0.2, 0, self.dispatch_entity_munitions_callback) for n in range(int(count))])
            count = 3.0
            self.dispatch_callback([EncrypterDrone(n*-100, -200, -2300 + n*-110, 700, n/count*-math.pi/4.0, math.pi/2.0, 190, now+n*0.2, 0.5+(n/count*0.5), self.dispatch_entity_munitions_callback) for n in range(int(count))])
            self.dispatch_entity_munitions_callback([EncryptionMunition(20*(n/6.0 - 0.5), -200, -2500+(n*100), -48-random.randrange(5)) for n in range(6)])
            self.wave_counter += 1
            if self.wave_counter > 4:
                self.mode = 0
                self.wave_counter = 0
                print(self.mode)


class MenuView(arcade.View):
    def on_show_view(self):
        self.story = arcade.load_texture(os.path.join('.', 'assets', 'story.png'))
        self.title = arcade.Text(
            "TUX IMPERIUM", self.window.width // 2,
            self.window.height // 2 + 60 + self.story.height // 2 + 10,
            (200, 0, 0, 255), 48,
            anchor_x='center', font_name='Logic twenty-five A',
        )

    def on_draw(self):
        self.clear()
        cx = self.window.width // 2
        cy = self.window.height // 2
        arcade.draw_texture_rect(
            self.story,
            arcade.XYWH(cx, cy, self.story.width, self.story.height),
        )
        self.title.draw()

    def on_mouse_release(self, x, y, button, modifiers):
        self.window.show_view(GameView())

    def on_key_release(self, symbol, modifiers):
        if symbol != arcade.key.F and symbol != arcade.key.ESCAPE:
            self.window.show_view(GameView())


class GameView(arcade.View):
    def on_show_view(self):
        self.camera = imptux.Camera()
        self.toggle_camera_mode(DEBUG)
        self.toggle_game_music(not DEBUG)

        self.help_texture = arcade.load_texture(os.path.join('.', 'assets', 'help.png'))
        self.help_mode = False

        self.score_label = arcade.Text(
            "00000000", self.window.width - 10, self.window.height - 60,
            (200, 0, 0, 255), 48,
            anchor_x='right', font_name='Logic twenty-five A',
        )
        self.health_label = arcade.Text(
            "000", 10, self.window.height - 60,
            (200, 0, 0, 255), 48,
            font_name='Logic twenty-five A',
        )
        self.notification_label = arcade.Text(
            "", self.window.width // 2, self.window.height // 2,
            (200, 0, 0, 255), 84,
            anchor_x='center', font_name='Logic twenty-five A',
        )
        self.current_level = None
        self.notification_timestamp = 0
        self.fire_a = False
        self.fire_b = False
        self.new_game()

    def on_hide_view(self):
        if hasattr(self, 'music_player') and self.music_player:
            arcade.stop_sound(self.music_player)
            self.music_player = None

    def status_check(self, dt):
        print(len(self.collision_entities), len(self.collision_entities_b),
              len(self.munitions_a), len(self.munitions_b), len(self.munitions_c))

    def notify(self, what, duration=3.0):
        self.notification_label.value = str(what)
        self.notification_timestamp = time.time() + duration

    def new_game(self):
        self.collision_entities = []
        self.collision_entities_b = []
        self.munitions_a = []
        self.munitions_b = []
        self.munitions_c = []
        self.terrain = Terrain(0, -200, 0)
        self.player = Player(0, 0, -100)
        self.score = 0
        self.current_level = LevelOne(
            self.dispatch_entities_callback,
            self.dispatch_entities_b_callback,
            self.dispatch_entity_munitions_callback,
        )
        self.notify(self.current_level.label)
        self.toggle_game_music(not DEBUG)

    def dispatch_entities_callback(self, entities):
        self.collision_entities.extend(entities)

    def dispatch_entities_b_callback(self, entities):
        self.collision_entities_b.extend(entities)

    def dispatch_entity_munitions_callback(self, entities):
        self.munitions_c.extend(entities)

    def on_update(self, dt):
        now = time.time()
        self.current_level.update(dt)
        self.player.update(dt, now)
        if self.player.health <= 0:
            print("Game over! Your final score was %d" % self.score)
            self.new_game()

        self.terrain.update(dt)
        player = self.player

        cooldown_rate = -10

        if self.fire_a:
            munitions = self.player.fire(now, 0)
            if munitions:
                self.munitions_a.extend(munitions)
                if self.fire_b:
                    self.player.weapon_b_cooldown = min(100, self.player.weapon_b_cooldown + 1)
        else:
            self.player.weapon_a_cooldown = max(0, self.player.weapon_a_cooldown + cooldown_rate * dt)

        if self.fire_b:
            munitions = self.player.fire(now, 1)
            if munitions:
                if self.fire_a:
                    self.player.weapon_a_cooldown = min(100, self.player.weapon_a_cooldown + 1)
                self.munitions_b.extend(munitions)
        else:
            self.player.weapon_b_cooldown = max(0, self.player.weapon_b_cooldown + cooldown_rate * dt)

        temp = []
        for entity in self.collision_entities:
            if entity.update(dt, now):
                if (entity.left <= player.right and player.left <= entity.right and
                        entity.bottom <= player.top and player.bottom <= entity.top):
                    entity.collision_player(player)
                    player.collision_entity(entity)
                else:
                    temp.append(entity)
            else:
                self.score += 100
        self.collision_entities = temp

        temp = []
        for entity in self.collision_entities_b:
            if entity.update(dt, now):
                temp.append(entity)
            else:
                self.score += 1000
        self.collision_entities_b = temp

        temp = []
        for entity in self.munitions_c:
            if entity.update(dt, now):
                if (entity.left <= player.right and player.left <= entity.right and
                        entity.bottom <= player.top and player.bottom <= entity.top):
                    entity.collision_player(player)
                    player.collision_entity_munition(entity)
                else:
                    temp.append(entity)
        self.munitions_c = temp

        temp = []
        for munition in self.munitions_a:
            if munition.update(dt):
                for entity in self.collision_entities:
                    if (entity.left <= munition.right and munition.left <= entity.right and
                            entity.bottom <= munition.top and munition.bottom <= entity.top):
                        entity.collision(munition)
                        munition.collision(entity)
                        break
                for entity in self.collision_entities_b:
                    if (entity.left <= munition.right and munition.left <= entity.right and
                            entity.bottom <= munition.top and munition.bottom <= entity.top):
                        munition.collision(entity)
                        break
                temp.append(munition)
        self.munitions_a = temp

        temp = []
        for munition in self.munitions_b:
            if munition.update(dt):
                for entity in self.collision_entities_b:
                    if (entity.left <= munition.right and munition.left <= entity.right and
                            entity.bottom <= munition.top and munition.bottom <= entity.top):
                        entity.collision(munition)
                        munition.collision(entity)
                        break
                for entity in self.collision_entities:
                    if (entity.left <= munition.right and munition.left <= entity.right and
                            entity.bottom <= munition.top and munition.bottom <= entity.top):
                        munition.collision(entity)
                        break
                temp.append(munition)
        self.munitions_b = temp

    def toggle_camera_mode(self, debug=False):
        self.camera_debug_mode = debug
        if self.camera_debug_mode:
            self.camera.x, self.camera.y, self.camera.z = (0.0, 1344, 2348)
            self.camera.rx, self.camera.ry = (87.0, 0.0)
            self.camera.fieldofview = 60
        else:
            self.camera.x, self.camera.y, self.camera.z = (-4.29767643203, -178, 34)
            self.camera.rx, self.camera.ry = (-13.25, -22.5)
            self.camera.fieldofview = 90
            self.camera.clipfar = 7000
        self.camera.defaultView(self.window.width, self.window.height)

    def toggle_game_music(self, active=True):
        self.playing_music = active
        if not hasattr(self, 'music_player'):
            self.music_player = None
        if self.playing_music:
            pass
        else:
            pass

    def on_draw(self):
        self.clear()
        if not self.player:
            return
        self.camera.x = self.player.x / 1.5
        if self.camera_debug_mode:
            self.camera.position()
        else:
            self.camera.position((0, 0, -100000))
        rz = self.player.x / 200.0
        gl.glRotatef(-5 * rz, 0, 0, 1)
        self.terrain.draw()
        gl.glEnable(gl.GL_DEPTH_TEST)
        for entity in self.collision_entities:
            entity.draw()
        for entity in self.collision_entities_b:
            entity.draw()
        for munition in self.munitions_a:
            munition.draw()
        for munition in self.munitions_b:
            munition.draw()
        for munition in self.munitions_c:
            munition.draw()
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.player.draw()

        # Draw HUD
        self.health_label.value = "%03d (%03d:%03d)" % (
            self.player.health, self.player.weapon_a_cooldown, self.player.weapon_b_cooldown)
        self.score_label.value = "%08d" % self.score
        self.health_label.draw()
        self.score_label.draw()

        if self.notification_timestamp > time.time():
            nw = self.notification_label.content_width
            nh = self.notification_label.content_height
            cx = self.window.width // 2
            cy = self.window.height // 2
            arcade.draw_lrbt_rectangle_filled(
                cx - nw // 2 - 3, cx + nw // 2 + 3,
                cy - 3, cy + nh + 3,
                (0, 0, 0, 128),
            )
            self.notification_label.draw()

        if self.help_mode:
            cx = self.window.width // 2
            cy = self.window.height // 2
            arcade.draw_texture_rect(
                self.help_texture,
                arcade.XYWH(cx, cy, self.help_texture.width, self.help_texture.height),
            )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.A:
            self.player.move_left(1)
        elif symbol == arcade.key.D:
            self.player.move_right(1)
        elif symbol == arcade.key.J:
            self.fire_a = True
        elif symbol == arcade.key.K:
            self.fire_b = True
        elif symbol == arcade.key.C:
            print('camera: x=%s y=%s z=%s rx=%s ry=%s' % (
                self.camera.x, self.camera.y, self.camera.z,
                self.camera.rx, self.camera.ry))
        elif symbol == arcade.key.F1:
            self.toggle_camera_mode(not self.camera_debug_mode)
        elif symbol == arcade.key.M:
            self.toggle_game_music(not self.playing_music)
        elif symbol == arcade.key.H:
            self.help_mode = not self.help_mode

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.A:
            self.player.move_left(0)
        elif symbol == arcade.key.D:
            self.player.move_right(0)
        elif symbol == arcade.key.J:
            self.fire_a = False
        elif symbol == arcade.key.K:
            self.fire_b = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire_a = True
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.fire_b = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire_a = False
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.fire_b = False

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.camera.defaultView(width, height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not modifiers & arcade.key.MOD_ALT:
            return
        if buttons == 1:
            self.camera.x -= dx * 2
            self.camera.y -= dy * 2
        elif buttons == 2:
            self.camera.x -= dx * 2
            self.camera.z -= dy * 2
        elif buttons == 4:
            self.camera.ry += dx / 4.
            self.camera.rx -= dy / 4.


class TuxImperium(arcade.Window):
    def __init__(self):
        super().__init__(1000, 500, "Tux Imperium")
        from imptux.renderer import renderer
        renderer.init(self.ctx)
        arcade.load_font(os.path.join('.', 'assets', 'l25a__.TTF'))
        self.show_view(MenuView())

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()
        elif symbol == arcade.key.S:
            arcade.get_image().save('screenshot-%d.png' % int(time.time()))
            return True
        elif symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)


def main():
    TuxImperium()
    arcade.run()


if __name__ == '__main__':
    main()
