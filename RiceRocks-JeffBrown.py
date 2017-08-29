# http://www.codeskulptor.org/#user40_we3AeoJhRB_17.py
# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
FAR_ENOUGH_AWAY = 200
score = 0
lives = 3
time = 0
started = False
sound_is_on = True

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            if sound_is_on:
                ship_thrust_sound.rewind()
                ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        # Phase 3 - 1b/c
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        # Phase 3 - 3a/d -- missiles need lifespan
        a_missile.lifespan = 50
        # Phase 3 - 1c (complete)
        missile_group.add(a_missile)
    
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound and sound_is_on:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]),
                              self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Phase 3 - 3b/d (check age to lifespan)
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
        
    #Phase 2 - 1
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) < self.radius + other_object.radius:
            return True
        else:
            return False
  
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, my_ship
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    soundtrack.rewind()
    if (not started) and inwidth and inheight:
        started = True
        # Phase 5 - 2a initialize score, lives
        score = 0
        lives = 3
        # Phase 5 - 2b re-initialize ship position
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0,0]
        my_ship.angle = 0
        if sound_is_on:
            soundtrack.play()


def draw(canvas):
    global time, started, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites, update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    # Phase 1 - 4 (complete)
    process_sprite_group(rock_group, canvas)
    # Phase 3 - 2 (complete)
    process_sprite_group(missile_group, canvas)
    # Phase 2 - 3 (complete)
    if group_collide(rock_group, my_ship):
        lives -= 1
    # Phase 4b/b (complete)
    score += group_group_collide(rock_group, missile_group)
    process_sprite_group(explosion_group, canvas)

# Phase 1 - 3a/b -- move update into process_sprite_group
#    for a_rock in rock_group:
#        a_rock.update()
#    for a_missile in missile_group:
#        a_missile.update()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    if not sound_is_on:
        soundtrack.pause()
    
    # Phase 5 - 1a/b 
    if not lives > 0:
        started = False
        if sound_is_on:
            soundtrack.pause()
        discard_rock_group = set(rock_group)
        for each_rock in discard_rock_group:
            rock_group.discard(each_rock)

# Phase 1 - 3b/b (complete)
def process_sprite_group(sprite_group, canvas):
    # BEGIN Phase 4 - 4a/b
    temp_2bremoved = set([])
    removal_happened = False
    # END Phase 3 - 4a/b
    for a_sprite in sprite_group:
        a_sprite.draw(canvas)
# Phase 3 - 4b/b (complete, Phase 3 complete)
        if a_sprite.update():
            temp_2bremoved.add(a_sprite)
            removal_happened = True
    if removal_happened:
        for a_sprite in temp_2bremoved:
            sprite_group.remove(a_sprite)

# Phase 2 - 2 (complete)
def group_collide(set_group, other_object):
    global explosion_group
    temp_2bremoved = set([])
    collision_happened = False
    for a_rock in set_group:
        if a_rock.collide(other_object):
            temp_2bremoved.add(a_rock)
            collision_happened = True
    if collision_happened:
        for a_rock in temp_2bremoved:
            set_group.remove(a_rock)
            an_explosion = Sprite(a_rock.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
    return collision_happened

# Phase 4a/b helper function
def group_group_collide(set_group_a, set_group_b):
    temp_2bremoved_a = set([])
    collision_count = 0
    for each_sprite_a in set_group_a:
        if group_collide(set_group_b, each_sprite_a):
            collision_count += 1
            temp_2bremoved_a.add(each_sprite_a)
    if collision_count > 0:
        for each_removal in temp_2bremoved_a:
            set_group_a.discard(each_removal)
    return collision_count
        
# timer handler that spawns a rock    
def rock_spawner():
# Phase One - 2 (complete)
    global rock_group
    # Phase 5 - 1b/b add started conditional (complete)
    if started:
        if len(rock_group) < 12:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            # Phase 5 - 3 if a rock is too close to the ship keep randomizing till it's not
            while dist(my_ship.pos, rock_pos) < FAR_ENOUGH_AWAY:
                rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
            rock_avel = random.random() * .2 - .1
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)

def sound_button_click():
    global sound_is_on
    if sound_is_on:
        sound_is_on = False
    else:
        sound_is_on = True
        if started:
            soundtrack.rewind()
            soundtrack.play()
            

# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
# Phase 5 - 2b move ship initialization to click handler
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
# Phase One - 1 (complete)
# a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
rock_group = set([])
# Phase 3 - 1a/c
# a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
# optional sound on/off switch for quiet play
# sound_button = frame.add_button("Sound On/Off", sound_button_click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
