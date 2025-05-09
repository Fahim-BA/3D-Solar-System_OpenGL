# Imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random

# --- Constants ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
FOV_Y = 60.0 # Field of View in Y direction
NEAR_CLIP = 0.1
FAR_CLIP = 5000.0 # Increased far clip to see Neptune clearly

# for gravity
GRAVITY_FACTOR = 1.0 # Normal gravity (1.0 = default)
GRAVITY_STEP = 0.1 # How much to change gravity with each key press

# Planet/Sun Sizes (Approximate relative scale)
SUN_RADIUS = 30.0 # Reduced sun size for better viewing
MERCURY_RADIUS = 4.0
VENUS_RADIUS = 8.0
EARTH_RADIUS = 9.0
MARS_RADIUS = 7.0
JUPITER_RADIUS = 25.0
SATURN_RADIUS = 20.0
SATURN_RING_INNER = 25.0
SATURN_RING_OUTER = 35.0
URANUS_RADIUS = 15.0
NEPTUNE_RADIUS = 14.0

# Planet Orbital Radii
MERCURY_ORBIT_RADIUS = 70.0
VENUS_ORBIT_RADIUS = 100.0
EARTH_ORBIT_RADIUS = 150.0
MARS_ORBIT_RADIUS = 200.0
JUPITER_ORBIT_RADIUS = 300.0
SATURN_ORBIT_RADIUS = 400.0
URANUS_ORBIT_RADIUS = 470.0
NEPTUNE_ORBIT_RADIUS = 530.0

# Asteroid Belt Parameters
ASTEROID_BELT_INNER_RADIUS = 220.0
ASTEROID_BELT_OUTER_RADIUS = 280.0
NUM_ASTEROIDS = 250 # Increased for denser belt
ASTEROID_MIN_SIZE = 0.5
ASTEROID_MAX_SIZE = 2.5
ASTEROID_BELT_HEIGHT = 15.0 # Max deviation from ecliptic

# Starfield Parameters
NUM_STARS = 300
STARFIELD_RADIUS = 1500 # Make starfield larger

# Sphere Tessellation Quality
SPHERE_SLICES = 30
SPHERE_STACKS = 30
RING_SLICES = 50
RING_LOOPS = 5

# Rotation Speeds (radians per frame - adjusted for visual appeal)
MERCURY_ORBIT_SPEED = 0.0100
VENUS_ORBIT_SPEED = 0.0070
EARTH_ORBIT_SPEED = 0.0050
MARS_ORBIT_SPEED = 0.0040
JUPITER_ORBIT_SPEED = 0.0020
SATURN_ORBIT_SPEED = 0.0015
URANUS_ORBIT_SPEED = 0.0010
NEPTUNE_ORBIT_SPEED = 0.0008
ASTEROID_ORBIT_SPEED = 0.001 # Base speed for asteroid rotation

# Planet Self-Rotation Speeds (Degrees per frame)
EARTH_ROTATION_SPEED = 0.5 # Example: Earth rotates faster

# --- Scene Objects ---
stars = []
asteroids = []
ring_quadric = None # For Saturn's rings

# --- Simulation State ---
mercury_orbit_angle = 0.0
venus_orbit_angle = 0.0
earth_orbit_angle = 0.0
mars_orbit_angle = 0.0
jupiter_orbit_angle = 0.0
saturn_orbit_angle = 0.0
uranus_orbit_angle = 0.0
neptune_orbit_angle = 0.0
moon_orbit_angle = 0.0 # Add with other orbit angles
earth_rotation_angle = 0.0 # Separate from orbit angle

# --- Moon Parameters ---
# Earth (already done)
MOON_RADIUS = 2.5
MOON_ORBIT_RADIUS = 15.0
MOON_ORBIT_SPEED = 0.02
MOON_MATERIAL = [0.7, 0.7, 0.7, 1.0] # Gray (Earth's Moon)

# Mars (Phobos & Deimos)
PHOBOS_RADIUS = 1.2
PHOBOS_ORBIT_RADIUS = 9.0
PHOBOS_ORBIT_SPEED = 0.03
PHOBOS_MATERIAL = [0.5, 0.4, 0.3, 1.0] # Dark gray

DEIMOS_RADIUS = 0.8
DEIMOS_ORBIT_RADIUS = 12.0
DEIMOS_ORBIT_SPEED = 0.025
DEIMOS_MATERIAL = [0.4, 0.3, 0.2, 1.0] # Reddish-gray

# Jupiter (4 Galilean moons)
IO_RADIUS = 3.0
IO_ORBIT_RADIUS = 30.0
IO_ORBIT_SPEED = 0.04
IO_MATERIAL = [0.9, 0.6, 0.3, 1.0] # Sulfur yellow

EUROPA_RADIUS = 2.8
EUROPA_ORBIT_RADIUS = 45.0
EUROPA_ORBIT_SPEED = 0.035
EUROPA_MATERIAL = [0.8, 0.8, 0.9, 1.0] # Ice white

GANYMEDE_RADIUS = 4.0
GANYMEDE_ORBIT_RADIUS = 60.0
GANYMEDE_ORBIT_SPEED = 0.03
GANYMEDE_MATERIAL = [0.6, 0.6, 0.7, 1.0] # Pale blue

CALLISTO_RADIUS = 3.8
CALLISTO_ORBIT_RADIUS = 75.0
CALLISTO_ORBIT_SPEED = 0.025
CALLISTO_MATERIAL = [0.5, 0.5, 0.5, 1.0] # Gray

# Saturn (Titan - largest moon)
TITAN_RADIUS = 4.5
TITAN_ORBIT_RADIUS = 50.0
TITAN_ORBIT_SPEED = 0.02
TITAN_MATERIAL = [0.8, 0.6, 0.4, 1.0] # Orange haze

# Uranus (Titania - largest moon)
TITANIA_RADIUS = 3.2
TITANIA_ORBIT_RADIUS = 40.0
TITANIA_ORBIT_SPEED = 0.015
TITANIA_MATERIAL = [0.7, 0.7, 0.8, 1.0] # Icy blue

# Neptune (Triton - largest moon)
TRITON_RADIUS = 3.5
TRITON_ORBIT_RADIUS = 35.0
TRITON_ORBIT_SPEED = 0.018
TRITON_MATERIAL = [0.6, 0.7, 0.8, 1.0] # Frozen nitrogen

# Moon orbit angles (add near other orbit angles)
phobos_orbit_angle = 0.0
deimos_orbit_angle = 0.0
io_orbit_angle = 0.0
europa_orbit_angle = 0.0
ganymede_orbit_angle = 0.0
callisto_orbit_angle = 0.0
titan_orbit_angle = 0.0
titania_orbit_angle = 0.0
triton_orbit_angle = 0.0

# Sun glow parameters
SUN_GLOW_LAYERS = 5
SUN_GLOW_RADIUS = SUN_RADIUS * 1.5
SUN_GLOW_COLORS = [
    [1.0, 0.9, 0.7, 0.8], # Inner glow (bright)
    [1.0, 0.8, 0.6, 0.6],
    [1.0, 0.7, 0.5, 0.4],
    [1.0, 0.6, 0.4, 0.2],
    [1.0, 0.5, 0.3, 0.1] # Outer glow (faint)
]

# --- Camera ---
# Initial camera position slightly above Earth's orbit plane, looking at the Sun
camera_pos = [0.0, 40.0, EARTH_ORBIT_RADIUS + 60.0] # Start slightly further back
camera_target = [0.0, 0.0, 0.0] # Look at the origin (Sun)
camera_up = [0.0, 1.0, 0.0] # Y is up

CAMERA_MOVE_SPEED = 10.0
CAMERA_ZOOM_SPEED = 10.0

# --- Lighting ---
sun_light_position = [0.0, 0.0, 0.0, 1.0] # Positioned at the Sun (origin)
sun_light_diffuse = [1.0, 1.0, 0.9, 1.0] # Sunlight color (slightly yellow)
sun_light_ambient = [0.1, 0.1, 0.1, 1.0] # Minimal ambient light
sun_light_specular = [0.8, 0.8, 0.8, 1.0] # White specular highlights

material_specular = [1.0, 1.0, 1.0, 1.0] # Material specular reflection color (white)
material_shininess = 50.0 # Material shininess exponent

# Planet Materials (Ambient and Diffuse properties)
# Using lists [R, G, B, Alpha]
MAT_SUN = [1.0, 0.8, 0.0, 1.0] # Sun is emissive, but use color when lighting off
MAT_MERCURY = [0.6, 0.6, 0.6, 1.0] # Grey
MAT_VENUS = [0.8, 0.7, 0.5, 1.0] # Yellowish-brown
MAT_EARTH = [0.2, 0.4, 0.8, 1.0] # Blue/Green dominant
MAT_MARS = [0.8, 0.3, 0.1, 1.0] # Reddish
MAT_JUPITER = [0.7, 0.6, 0.4, 1.0] # Orangey-brown bands
MAT_SATURN = [0.8, 0.75, 0.6, 1.0] # Pale yellow
MAT_SATURN_RING = [0.8, 0.7, 0.6, 0.7] # Pale gold color with some transparency
MAT_URANUS = [0.6, 0.8, 0.9, 1.0] # Pale blue/cyan
MAT_NEPTUNE = [0.3, 0.5, 0.9, 1.0] # Deeper blue

# --- Camera Director Constants ---
CAMERA_MODE_FREE = 0        # Free camera (original implementation)
CAMERA_MODE_FIRST_PERSON = 1  # First-person view (astronaut helmet)
CAMERA_MODE_THIRD_PERSON = 2  # Third-person view (behind rocket)
CAMERA_MODE_CRASH = 3       # Crash camera (tracks falling rocket)

# Rocket Constants
ROCKET_LENGTH = 12.0        # Length of the rocket
ROCKET_RADIUS = 2.5         # Radius of the rocket body
ROCKET_THRUST_LENGTH = 5.0  # Length of the rocket thrust flame
ROCKET_ORBIT_RADIUS = 170.0 # Default orbit radius (between Earth and Mars)
ROCKET_ORBIT_SPEED = 0.003  # Default orbit speed
ROCKET_ROTATION_SPEED = 3.0 # Rotation speed of the rocket (degrees per frame)

# Camera Constants
FIRST_PERSON_OFFSET = [0.0, 2.0, 0.0]  # Offset from rocket position for first-person view
THIRD_PERSON_DISTANCE = 20.0           # Distance behind rocket for third-person view
THIRD_PERSON_HEIGHT = 5.0              # Height above rocket for third-person view

# Keys for camera mode switching
KEY_FREE_CAMERA = b'0'
KEY_FIRST_PERSON = b'1'
KEY_THIRD_PERSON = b'2'
KEY_CRASH_CAMERA = b'3'
KEY_START_CRASH = b'c'      # Trigger crash sequence

# Rocket State Variables
rocket_position = [0.0, 0.0, ROCKET_ORBIT_RADIUS]  # Initial position
rocket_velocity = [0.0, 0.0, 0.0]                  # Initial velocity
rocket_orientation = [0.0, 1.0, 0.0]               # Up vector (y-axis)
rocket_heading = [1.0, 0.0, 0.0]                   # Forward vector (initially along x-axis)
rocket_orbit_angle = 0.0                           # Current orbit angle
rocket_rotation_angle = 0.0                        # Rotation angle of rocket model

# Crash Animation Variables
is_crashing = False                  # Is rocket currently in crash sequence?
crash_start_time = 0                 # Time when crash sequence started
crash_duration = 5.0                 # Duration of crash sequence in seconds
crash_target = [0.0, 0.0, 0.0]       # Target position for crash (the Sun)
crash_start_position = [0.0, 0.0, 0.0]  # Starting position when crash initiated
crash_camera_distance = 40.0         # Distance for crash camera view
crash_progress = 0.0                 # Progress of crash animation (0.0 to 1.0)
crash_spin_speed = 10.0              # How fast rocket spins during crash
crash_tumble_factor = 5.0            # How much rocket tumbles during crash

# Camera State Variables
current_camera_mode = CAMERA_MODE_FREE  # Start with free camera mode
free_camera_pos = [0.0, 40.0, ROCKET_ORBIT_RADIUS + 60.0]  # Same as original
free_camera_target = [0.0, 0.0, 0.0]    # Looking at the Sun initially
free_camera_up = [0.0, 1.0, 0.0]        # Y is up

# --- Initialization Functions ---
def initialize_stars():
    """Populates the 'stars' list with random 3D coordinates."""
    global stars
    stars = []
    for _ in range(NUM_STARS):
        # Distribute stars on the surface of a large sphere
        phi = random.uniform(0, 2 * math.pi)
        costheta = random.uniform(-1, 1)
        theta = math.acos(costheta)
        x = STARFIELD_RADIUS * math.sin(theta) * math.cos(phi)
        y = STARFIELD_RADIUS * math.sin(theta) * math.sin(phi)
        z = STARFIELD_RADIUS * math.cos(theta)
        stars.append((x, y, z))

def initialize_asteroids():
    """Populates the 'asteroids' list with positions, sizes, and colors."""
    global asteroids
    asteroids = []
    for _ in range(NUM_ASTEROIDS):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(ASTEROID_BELT_INNER_RADIUS, ASTEROID_BELT_OUTER_RADIUS)
        height = random.uniform(-ASTEROID_BELT_HEIGHT, ASTEROID_BELT_HEIGHT) # Deviation from Y=0 plane
        x = distance * math.cos(angle)
        z = distance * math.sin(angle)
        y = height
        size = random.uniform(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        color_val = random.uniform(0.3, 0.7) # Grayish colors
        color = [color_val, color_val, color_val, 1.0]
        # Store initial angle and distance for rotation in idle()
        asteroids.append({
            "x": x, "y": y, "z": z,
            "size": size, "color": color,
            "angle": angle, "distance": distance, "height": y # Store orbital parameters
        })

def initialize_scene():
    """Initializes stars, asteroids, and Saturn's ring quadric."""
    global ring_quadric
    print("Initializing Scene...")
    initialize_stars()
    initialize_asteroids()
    # Create quadric for Saturn's rings
    ring_quadric = gluNewQuadric()
    gluQuadricNormals(ring_quadric, GLU_SMOOTH)
    gluQuadricTexture(ring_quadric, GL_TRUE) # Enable if adding textures later
    print("Initialization Complete.")

# --- Helper Functions for Camera Director ---
def normalize(v):
    """Normalize a vector to unit length."""
    length = math.sqrt(sum(x*x for x in v))
    if length > 0:
        return [x/length for x in v]
    return v

def cross_product(a, b):
    """Compute the cross product of two 3D vectors."""
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def scale_vector(v, s):
    """Scale a vector by a scalar."""
    return [x*s for x in v]

def add_vectors(a, b):
    """Add two vectors."""
    return [a[i] + b[i] for i in range(len(a))]

def subtract_vectors(a, b):
    """Subtract vector b from vector a."""
    return [a[i] - b[i] for i in range(len(a))]

def length(v):
    """Calculate the length of a vector."""
    return math.sqrt(sum(x*x for x in v))

# --- Drawing Functions ---
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draws text on the screen using bitmap fonts."""
    viewport = glGetIntegerv(GL_VIEWPORT)
    win_width, win_height = viewport[2], viewport[3]
    
    # Convert to percentage-based positioning if needed
    x_pos = x
    y_pos = y
    
    glColor3f(1.0, 1.0, 1.0) # White text
    glWindowPos2f(x_pos, y_pos)
    
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def draw_earth():
    glPushMatrix()
    glRotatef(math.degrees(earth_orbit_angle), 0, 1, 0) # Orbit around Sun
    glTranslatef(EARTH_ORBIT_RADIUS, 0, 0)
    
    # Use the separate rotation angle
    glRotatef(earth_rotation_angle, 0, 1, 0) # Rotates around Earth's axis
    
    # Smoother day/night effect with more slices
    slices = 36 # Increased from your original 10
    stacks = 36 # Increased from your original 10
    
    for i in range(0, 180, 5): # More frequent latitude bands (5° steps)
        glBegin(GL_QUAD_STRIP)
        for j in range(0, 360, 5): # More frequent longitude bands (5° steps)
            # Vertex 1
            x = EARTH_RADIUS * math.sin(math.radians(i)) * math.cos(math.radians(j))
            y = EARTH_RADIUS * math.cos(math.radians(i))
            z = EARTH_RADIUS * math.sin(math.radians(i)) * math.sin(math.radians(j))
            
            # Simple day/night based on x position (sun is at 0,0,0)
            if x > 0: # Day side
                glColor3f(0.2, 0.4, 0.8) # Ocean blue
            else: # Night side
                glColor3f(0.05, 0.05, 0.1) # Dark blue
            
            glVertex3f(x, y, z)
            
            # Vertex 2 (next latitude)
            x = EARTH_RADIUS * math.sin(math.radians(i+5)) * math.cos(math.radians(j))
            y = EARTH_RADIUS * math.cos(math.radians(i+5))
            z = EARTH_RADIUS * math.sin(math.radians(i+5)) * math.sin(math.radians(j))
            
            if x > 0:
                glColor3f(0.2, 0.4, 0.8)
            else:
                glColor3f(0.05, 0.05, 0.1)
            
            glVertex3f(x, y, z)
        glEnd()
    
    # Draw Earth's moon
    glPushMatrix()
    glColor4fv(MOON_MATERIAL)
    glRotatef(math.degrees(moon_orbit_angle), 0, 1, 0)
    glTranslatef(MOON_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(MOON_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    glPopMatrix()

def draw_starfield():
    """Draws the starfield using GL_POINTS."""
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0) # White stars
    for x, y, z in stars:
        glVertex3f(x, y, z)
    glEnd()

def draw_orbit_lines():
    """Draws circular orbit lines for each planet."""
    glLineWidth(1)
    glColor3f(0.3, 0.3, 0.3) # Dim grey lines
    
    orbit_radii = [
        MERCURY_ORBIT_RADIUS, VENUS_ORBIT_RADIUS, EARTH_ORBIT_RADIUS,
        MARS_ORBIT_RADIUS, JUPITER_ORBIT_RADIUS, SATURN_ORBIT_RADIUS,
        URANUS_ORBIT_RADIUS, NEPTUNE_ORBIT_RADIUS
    ]
    
    for radius in orbit_radii:
        glBegin(GL_LINE_LOOP)
        for i in range(100): # 100 segments for a smooth circle
            angle = i * 2 * math.pi / 100
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glVertex3f(x, 0, z) # Orbits are on the Y=0 plane
        glEnd()

def draw_asteroid_belt():
    """Draws the asteroid belt using GL_POINTS."""
    glPointSize(2) # Asteroids as small points
    glBegin(GL_POINTS)
    for asteroid in asteroids:
        # Set color directly using glColor3f for visibility without lighting
        glColor3f(asteroid["color"][0], asteroid["color"][1], asteroid["color"][2])
        # Draw the asteroid at its current position
        glVertex3f(asteroid["x"], asteroid["y"], asteroid["z"])
    glEnd()

def draw_saturn_with_rings():
    """Draws Saturn with its rings."""
    glPushMatrix() # Push 1 - Saturn's position
    
    # Position Saturn in its orbit
    glRotatef(math.degrees(saturn_orbit_angle), 0, 1, 0)
    glTranslatef(SATURN_ORBIT_RADIUS, 0, 0)
    
    # Draw Saturn
    glColor4fv(MAT_SATURN) # Set color directly for visibility
    glutSolidSphere(SATURN_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    
    # Draw rings
    glPushMatrix() # Push 2 - Rings position
    
    glColor4fv(MAT_SATURN_RING) # Set color directly for visibility
    
    # Rotate rings to match Saturn's axial tilt (about 26.7 degrees)
    glRotatef(-26.7, 0, 0, 1)
    
    # Draw the ring using a disk
    glRotatef(90, 1, 0, 0) # Rotate to lie in XZ plane
    gluDisk(ring_quadric, SATURN_RING_INNER, SATURN_RING_OUTER, RING_SLICES, RING_LOOPS)
    
    glPopMatrix() # Pop 2 - Rings position
    
    # Draw Titan (moon)
    glPushMatrix() # Push 3 - Moon position
    
    glColor4fv(TITAN_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(titan_orbit_angle), 0, 1, 0)
    glTranslatef(TITAN_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(TITAN_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    
    glPopMatrix() # Pop 3 - Moon position
    
    glPopMatrix() # Pop 1 - Saturn's position

def draw_sun_with_glow():
    """Draws the sun with a soft glowing edge effect."""
    # Draw glow layers (from outer to inner)
    for i in range(SUN_GLOW_LAYERS):
        radius = SUN_GLOW_RADIUS * (1.0 - i/SUN_GLOW_LAYERS)
        alpha = SUN_GLOW_COLORS[i][3]
        color = SUN_GLOW_COLORS[i]
        
        glPushMatrix()
        glColor4fv(color) # glColor is used when lighting is off
        glutSolidSphere(radius, SPHERE_SLICES*2, SPHERE_STACKS*2) # Higher resolution for smooth glow
        glPopMatrix()
    
    # Draw the core sun
    glPushMatrix()
    glColor4fv(MAT_SUN) # glColor is used when lighting is off
    glutSolidSphere(SUN_RADIUS, SPHERE_SLICES*2, SPHERE_STACKS*2)
    glPopMatrix()

def draw_solar_system():
    """Draws the Sun and planets with direct color setting."""
    global earth_orbit_angle, mars_orbit_angle, jupiter_orbit_angle, saturn_orbit_angle
    global mercury_orbit_angle, venus_orbit_angle, uranus_orbit_angle, neptune_orbit_angle
    
    # --- Sun (Source of Light) ---
    draw_sun_with_glow() # Note: Sun will not act as a light source without lighting enabled
    
    # --- Mercury ---
    glPushMatrix()
    glColor4fv(MAT_MERCURY) # Set color directly for visibility
    glRotatef(math.degrees(mercury_orbit_angle), 0, 1, 0) # Rotate orbit
    glTranslatef(MERCURY_ORBIT_RADIUS, 0, 0)
    # Add self-rotation here if desired
    glutSolidSphere(MERCURY_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    # --- Venus ---
    glPushMatrix()
    glColor4fv(MAT_VENUS) # Set color directly for visibility
    glRotatef(math.degrees(venus_orbit_angle), 0, 1, 0)
    glTranslatef(VENUS_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(VENUS_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    # --- Earth ---
    # Earth is drawn with manual per-vertex coloring in draw_earth()
    draw_earth()
    
    # --- Mars ---
    glPushMatrix()
    glColor4fv(MAT_MARS) # Set color directly for visibility
    glRotatef(math.degrees(mars_orbit_angle), 0, 1, 0)
    glTranslatef(MARS_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(MARS_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    
    # Phobos
    glPushMatrix()
    glColor4fv(PHOBOS_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(phobos_orbit_angle), 0, 1, 0)
    glTranslatef(PHOBOS_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(PHOBOS_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    # Deimos
    glPushMatrix()
    glColor4fv(DEIMOS_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(deimos_orbit_angle), 0, 1, 0)
    glTranslatef(DEIMOS_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(DEIMOS_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    glPopMatrix() # Mars
    
    # --- Jupiter ---
    glPushMatrix()
    glColor4fv(MAT_JUPITER) # Set color directly for visibility
    glRotatef(math.degrees(jupiter_orbit_angle), 0, 1, 0)
    glTranslatef(JUPITER_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(JUPITER_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    
    # Io
    glPushMatrix()
    glColor4fv(IO_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(io_orbit_angle), 0, 1, 0)
    glTranslatef(IO_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(IO_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    # Europa
    glPushMatrix()
    glColor4fv(EUROPA_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(europa_orbit_angle), 0, 1, 0)
    glTranslatef(EUROPA_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(EUROPA_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    # Ganymede
    glPushMatrix()
    glColor4fv(GANYMEDE_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(ganymede_orbit_angle), 0, 1, 0)
    glTranslatef(GANYMEDE_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(GANYMEDE_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    # Callisto
    glPushMatrix()
    glColor4fv(CALLISTO_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(callisto_orbit_angle), 0, 1, 0)
    glTranslatef(CALLISTO_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(CALLISTO_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    glPopMatrix() # Jupiter
    
    # --- Saturn ---
    draw_saturn_with_rings() # Note: Rings will not be transparent without blending enabled
    
    # --- Uranus ---
    glPushMatrix()
    glColor4fv(MAT_URANUS) # Set color directly for visibility
    glRotatef(math.degrees(uranus_orbit_angle), 0, 1, 0)
    glTranslatef(URANUS_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(URANUS_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    
    # Titania
    glPushMatrix()
    glColor4fv(TITANIA_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(titania_orbit_angle), 0, 1, 0)
    glTranslatef(TITANIA_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(TITANIA_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    glPopMatrix() # Uranus
    
    # --- Neptune ---
    glPushMatrix()
    glColor4fv(MAT_NEPTUNE) # Set color directly for visibility
    glRotatef(math.degrees(neptune_orbit_angle), 0, 1, 0)
    glTranslatef(NEPTUNE_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(NEPTUNE_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    
    # Triton
    glPushMatrix()
    glColor4fv(TRITON_MATERIAL) # Set color directly for visibility
    glRotatef(math.degrees(triton_orbit_angle), 0, 1, 0)
    glTranslatef(TRITON_ORBIT_RADIUS, 0, 0)
    glutSolidSphere(TRITON_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glPopMatrix()
    
    glPopMatrix() # Neptune

# --- Camera Director Functions ---
def update_rocket_position(delta_time=1.0):
    """Updates the rocket position based on its current state and orbit."""
    global rocket_position, rocket_heading, rocket_orbit_angle, rocket_rotation_angle
    
    if is_crashing:
        update_crash_sequence(delta_time)
        return
    
    # Update orbit angle
    rocket_orbit_angle = (rocket_orbit_angle + ROCKET_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    
    # Calculate rocket position in orbit
    rocket_position[0] = ROCKET_ORBIT_RADIUS * math.cos(rocket_orbit_angle)
    rocket_position[2] = ROCKET_ORBIT_RADIUS * math.sin(rocket_orbit_angle)
    
    # Calculate rocket heading (tangent to orbit)
    rocket_heading = normalize([-math.sin(rocket_orbit_angle), 0, math.cos(rocket_orbit_angle)])
    
    # Update rocket's rotation about its axis
    rocket_rotation_angle = (rocket_rotation_angle + ROCKET_ROTATION_SPEED) % 360.0

def update_crash_sequence(delta_time=1.0):
    """Updates the rocket during a crash sequence."""
    global rocket_position, rocket_heading, rocket_orientation, crash_progress
    
    # Update crash progress (0.0 to 1.0)
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0  # Convert to seconds
    elapsed = current_time - crash_start_time
    crash_progress = min(1.0, elapsed / crash_duration)
    
    if crash_progress >= 1.0:
        # Crash complete - reset
        reset_after_crash()
        return
    
    # Interpolation function with easing for more dramatic effect
    # Start slow, then accelerate towards the end
    t = crash_progress * crash_progress * (3.0 - 2.0 * crash_progress)
    
    # Linear interpolation between start position and Sun
    rocket_position = [
        crash_start_position[0] * (1-t) + crash_target[0] * t,
        crash_start_position[1] * (1-t) + crash_target[1] * t,
        crash_start_position[2] * (1-t) + crash_target[2] * t
    ]
    
    # Calculate direction vector to Sun for heading
    to_sun = normalize(subtract_vectors(crash_target, rocket_position))
    
    # Add tumbling/spinning to the rocket
    tumble_angle = crash_progress * crash_spin_speed * 720.0  # 2 full rotations
    
    # Create a tumbling effect by rotating the orientation vector
    # This creates a more chaotic crash appearance
    tumble_x = math.sin(tumble_angle * 0.7) * crash_tumble_factor * crash_progress
    tumble_z = math.cos(tumble_angle * 0.5) * crash_tumble_factor * crash_progress
    
    # Calculate rocket orientation with tumbling
    rocket_heading = to_sun
    rocket_orientation = normalize([tumble_x, 1.0 - crash_progress * 0.8, tumble_z])

def start_crash_sequence():
    """Initiates the rocket crash sequence."""
    global is_crashing, crash_start_time, crash_start_position
    
    if not is_crashing:
        is_crashing = True
        crash_start_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0  # Convert to seconds
        crash_start_position = rocket_position.copy()
        
        # If we're already in crash camera mode, keep it
        if current_camera_mode != CAMERA_MODE_CRASH:
            set_camera_mode(CAMERA_MODE_CRASH)

def reset_after_crash():
    """Resets the rocket after a crash sequence completes."""
    global is_crashing, rocket_position, rocket_orbit_angle, crash_progress
    
    is_crashing = False
    crash_progress = 0.0
    
    # Reset position to orbit
    rocket_orbit_angle = 0.0
    rocket_position = [ROCKET_ORBIT_RADIUS, 0.0, 0.0]
    
    # Reset camera to free mode
    set_camera_mode(CAMERA_MODE_FREE)

def set_camera_mode(mode):
    """Changes the camera mode to the specified mode."""
    global current_camera_mode
    current_camera_mode = mode

def update_camera():
    """Updates camera position and target based on current mode."""
    if current_camera_mode == CAMERA_MODE_FREE:
        return  # Free camera is controlled by keyboard directly
    elif current_camera_mode == CAMERA_MODE_FIRST_PERSON:
        update_first_person_camera()
    elif current_camera_mode == CAMERA_MODE_THIRD_PERSON:
        update_third_person_camera()
    elif current_camera_mode == CAMERA_MODE_CRASH:
        update_crash_camera()

def update_first_person_camera():
    """Updates camera to first-person (astronaut helmet) view."""
    global camera_pos, camera_target, camera_up
    
    # Calculate position: slightly forward and above the rocket center
    offset = FIRST_PERSON_OFFSET
    
    # Find a position at the front of the rocket
    position = add_vectors(rocket_position, scale_vector(rocket_heading, ROCKET_LENGTH * 0.5))
    position = add_vectors(position, offset)  # Add offset for helmet height
    
    # Look in the direction the rocket is heading
    target = add_vectors(position, rocket_heading)
    
    # Use rocket's up vector
    up = rocket_orientation
    
    # Update camera parameters
    camera_pos = position
    camera_target = target
    camera_up = up

def update_third_person_camera():
    """Updates camera to third-person view (behind rocket)."""
    global camera_pos, camera_target, camera_up
    
    # Camera position is behind and slightly above the rocket
    rocket_back = scale_vector(rocket_heading, -THIRD_PERSON_DISTANCE)
    rocket_up = scale_vector(rocket_orientation, THIRD_PERSON_HEIGHT)
    
    camera_pos = add_vectors(rocket_position, rocket_back)
    camera_pos = add_vectors(camera_pos, rocket_up)
    
    # Camera target is the rocket itself
    camera_target = rocket_position
    
    # Use rocket's up vector
    camera_up = rocket_orientation
    
    # Update camera parameters
    camera_pos = camera_pos
    camera_target = camera_target
    camera_up = camera_up

def update_crash_camera():
    """Updates camera to crash view (dramatic tracking of falling rocket)."""
    global camera_pos, camera_target, camera_up
    
    if not is_crashing:
        # If not currently crashing, position camera for dramatic effect
        # Looking at the rocket from a distance
        offset = scale_vector(normalize(rocket_position), crash_camera_distance)
        offset[1] += 20.0  # Add height for dramatic angle
        
        camera_pos = offset
        camera_target = rocket_position
        camera_up = [0.0, 1.0, 0.0]
    else:
        # During crash, create a dynamic camera that circles the rocket
        # as it crashes for dramatic effect
        
        # Calculate base position that's at a distance from the rocket
        # and slowly circles around it as it crashes
        circle_angle = crash_progress * math.pi * 4  # Two full circles during crash
        
        # Calculate circle position
        circle_x = math.cos(circle_angle) * crash_camera_distance
        circle_z = math.sin(circle_angle) * crash_camera_distance
        
        # Start higher and move lower as crash progresses
        height = 40.0 * (1.0 - crash_progress * 0.7)
        
        # Calculate camera position relative to rocket
        relative_pos = [circle_x, height, circle_z]
        
        # Convert to world coordinates
        camera_pos = add_vectors(rocket_position, relative_pos)
        camera_target = rocket_position
        
        # Dynamic up vector that tilts as crash progresses for more drama
        tilt = 0.3 * math.sin(crash_progress * math.pi * 3)
        camera_up = normalize([tilt, 1.0, tilt])
    
    # Update camera parameters
    camera_pos = camera_pos
    camera_target = camera_target
    camera_up = camera_up

def draw_rocket():
    """Draws the rocket at its current position with correct orientation."""
    glPushMatrix()
    
    # Position at rocket location
    glTranslatef(rocket_position[0], rocket_position[1], rocket_position[2])
    
    # Orient the rocket to face the direction of travel
    # Calculate the angle between the rocket's heading and the x-axis
    angle = math.degrees(math.atan2(rocket_heading[2], rocket_heading[0]))
    glRotatef(-angle, 0, 1, 0)  # Rotate around Y axis to face direction of travel
    
    # Add tumbling/spinning during crash
    if is_crashing:
        tumble_angle = crash_progress * crash_spin_speed * 720.0
        glRotatef(tumble_angle, 1, 0, 0)  # Roll
        glRotatef(tumble_angle * 0.7, 0, 0, 1)  # Yaw
    
    # Apply rocket's self-rotation
    glRotatef(rocket_rotation_angle, 0, 0, 1)
    
    # Draw the rocket body (cylinder + cone)
    draw_rocket_body()
    
    # Draw rocket engine thrust (if not crashing or at beginning of crash)
    if not is_crashing or crash_progress < 0.3:
        draw_rocket_thrust()
    
    glPopMatrix()

def draw_rocket_body():
    """Draws the rocket body components."""
    # Rocket Body (main cylinder)
    glPushMatrix()
    
    # Set color for rocket body
    glColor3f(0.8, 0.8, 0.9)  # Light metallic blue-grey
    
    # Create the quadric for the cylinder and cone
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    
    # Main body cylinder
    gluCylinder(quadric, ROCKET_RADIUS, ROCKET_RADIUS, ROCKET_LENGTH * 0.7, 20, 5)
    
    # Nose cone
    glPushMatrix()
    glTranslatef(0, 0, ROCKET_LENGTH * 0.7)
    gluCylinder(quadric, ROCKET_RADIUS, 0, ROCKET_LENGTH * 0.3, 20, 5)
    glPopMatrix()
    
    # Base cap (optional)
    gluDisk(quadric, 0, ROCKET_RADIUS, 20, 5)
    
    # Fins (4 triangular fins at the base)
    glPushMatrix()
    glColor3f(0.7, 0.2, 0.2)  # Reddish fins
    
    for i in range(4):
        glRotatef(90, 0, 0, 1)  # Rotate 90 degrees for each fin
        
        glBegin(GL_TRIANGLES)
        glNormal3f(0, 1, 0)  # Simple normal for lighting
        glVertex3f(0, 0, 0)  # Base of fin at rocket base
        glVertex3f(0, 0, ROCKET_LENGTH * 0.3)  # Fin extends along rocket
        glVertex3f(0, ROCKET_RADIUS * 1.5, 0)  # Fin extends outward
        glEnd()
    
    glPopMatrix()
    
    # Cleanup
    gluDeleteQuadric(quadric)
    
    glPopMatrix()

def draw_rocket_thrust():
    """Draws the rocket engine thrust flame."""
    glPushMatrix()
    
    # Draw at the base of the rocket, pointing backward
    glTranslatef(0, 0, 0)
    
    # Draw main thrust (cone shape)
    glBegin(GL_TRIANGLE_FAN)
    # Center of the base
    glColor3f(1.0, 1.0, 0.8)  # Bright yellow/white at center
    glVertex3f(0, 0, 0)
    
    # Edge points around the base
    num_segments = 20
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = ROCKET_RADIUS * 0.6 * math.cos(angle)
        y = ROCKET_RADIUS * 0.6 * math.sin(angle)
        glColor3f(1.0, 0.5, 0.0)  # Orange at the edges
        glVertex3f(x, y, 0)
    glEnd()
    
    # Draw the conical flame extending backward
    glBegin(GL_TRIANGLE_FAN)
    # Tip of the cone (back)
    glColor3f(1.0, 0.0, 0.0)  # Red at the tip
    glVertex3f(0, 0, -ROCKET_THRUST_LENGTH)
    
    # Base points
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = ROCKET_RADIUS * 0.6 * math.cos(angle)
        y = ROCKET_RADIUS * 0.6 * math.sin(angle)
        glColor3f(1.0, 0.5, 0.0)  # Orange at the base
        glVertex3f(x, y, 0)
    glEnd()
    
    glPopMatrix()

def draw_mode_info():
    """Draws information about the current camera mode."""
    # Get current viewport dimensions for text positioning
    viewport = glGetIntegerv(GL_VIEWPORT)
    win_width, win_height = viewport[2], viewport[3]
    
    # Display camera mode
    mode_text = "Unknown Mode"
    if current_camera_mode == CAMERA_MODE_FREE:
        mode_text = "Free Camera Mode (0) - Use WASDQE to move"
    elif current_camera_mode == CAMERA_MODE_FIRST_PERSON:
        mode_text = "First-Person Mode (1) - Astronaut Helmet View"
    elif current_camera_mode == CAMERA_MODE_THIRD_PERSON:
        mode_text = "Third-Person Mode (2) - Behind Rocket View"
    elif current_camera_mode == CAMERA_MODE_CRASH:
        mode_text = "Crash Camera Mode (3) - Press 'c' to trigger crash sequence"
        if is_crashing:
            mode_text += f" - Crash progress: {int(crash_progress * 100)}%"
    
    # Draw mode text
    draw_text(10, win_height - 40, mode_text)
    
    # Draw key info
    keys_text = "Keys: 0-3: Camera Modes | c: Crash Sequence | G/H: Gravity | ESC: Exit"
    draw_text(10, win_height - 60, keys_text)

def setup_lighting():
    """Configures OpenGL lighting. NOTE: Lighting will not be active without glEnable(GL_LIGHTING)."""
    # Set light properties - These calls do nothing without lighting enabled
    glLightfv(GL_LIGHT0, GL_POSITION, sun_light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sun_light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, sun_light_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, sun_light_specular) # Add specular component
    
    # Configure how light affects materials globally - These calls do nothing without lighting enabled
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE) # More realistic specular highlights
    
    # Set global material properties (can be overridden per object) - These calls do nothing without lighting enabled
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)
    
    # Use smooth shading for nicer visuals - glShadeModel affects rendering regardless of lighting
    glShadeModel(GL_SMOOTH)

def setupCamera():
    """Sets up the projection and modelview matrices for the camera."""
    # Projection Matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV_Y, float(WINDOW_WIDTH) / float(WINDOW_HEIGHT), NEAR_CLIP, FAR_CLIP)
    
    # ModelView Matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    cx, cy, cz = camera_pos
    tx, ty, tz = camera_target
    ux, uy, uz = camera_up
    
    gluLookAt(cx, cy, cz, tx, ty, tz, ux, uy, uz)

# --- GLUT Callback Functions ---
def keyboardListener(key, x, y):
    """Handles standard keyboard input."""
    global camera_pos, current_camera_mode, GRAVITY_FACTOR, EARTH_ROTATION_SPEED
    
    # Handle camera mode keys
    if key == KEY_FREE_CAMERA:
        set_camera_mode(CAMERA_MODE_FREE)
        print("Camera Mode: Free Camera")
    elif key == KEY_FIRST_PERSON:
        set_camera_mode(CAMERA_MODE_FIRST_PERSON)
        print("Camera Mode: First-Person (Astronaut View)")
    elif key == KEY_THIRD_PERSON:
        set_camera_mode(CAMERA_MODE_THIRD_PERSON)
        print("Camera Mode: Third-Person (Behind Rocket)")
    elif key == KEY_CRASH_CAMERA:
        set_camera_mode(CAMERA_MODE_CRASH)
        print("Camera Mode: Crash Camera")
    elif key == KEY_START_CRASH:
        start_crash_sequence()
        print("Crash Sequence Initiated!")
    else:
        # Pass other keys to original handler if we're in free camera mode
        if current_camera_mode == CAMERA_MODE_FREE:
            x_cam, y_cam, z_cam = camera_pos
            
            # Basic WASD for translation on X/Z plane, Q/E for up/down
            if key == b'w':
                z_cam -= CAMERA_MOVE_SPEED # Move forward
            elif key == b's':
                z_cam += CAMERA_MOVE_SPEED # Move backward
            elif key == b'a':
                x_cam -= CAMERA_MOVE_SPEED # Strafe left
            elif key == b'd':
                x_cam += CAMERA_MOVE_SPEED # Strafe right
            elif key == b'q': # Use Q for up
                y_cam += CAMERA_MOVE_SPEED # Move up
            elif key == b'e': # Use E for down
                y_cam -= CAMERA_MOVE_SPEED # Move down
            elif key == b'z': # Zoom in (move closer along view axis - simplified here)
                # A proper zoom would move towards the look-at point
                z_cam -= CAMERA_ZOOM_SPEED
            elif key == b'x': # Zoom out
                z_cam += CAMERA_ZOOM_SPEED
            elif key == b'g': # Increase gravity (faster orbits)
                GRAVITY_FACTOR = min(2.0, GRAVITY_FACTOR + GRAVITY_STEP)
            elif key == b'h': # Decrease gravity (slower orbits)
                GRAVITY_FACTOR = max(0.1, GRAVITY_FACTOR - GRAVITY_STEP)
            elif key == b',': # Slow down rotation
                EARTH_ROTATION_SPEED = max(0.1, EARTH_ROTATION_SPEED - 0.1)
            elif key == b'.': # Speed up rotation
                EARTH_ROTATION_SPEED = min(5.0, EARTH_ROTATION_SPEED + 0.1)
            elif key == b'\x1b': # Escape key
                glutLeaveMainLoop() # Exit the application
            
            camera_pos = [x_cam, y_cam, z_cam]
    
    glutPostRedisplay() # Request redraw after camera move

def specialKeyListener(key, x, y):
    """Handles special key input (arrows, function keys)."""
    pass # Not implemented for now

def mouseListener(button, state, x, y):
    """Handles mouse button clicks."""
    pass # Not implemented for now

def reshape(width, height):
    """Handle window resize while maintaining fixed aspect ratio"""
    # Calculate target aspect ratio (same as initial window)
    target_aspect = float(WINDOW_WIDTH) / float(WINDOW_HEIGHT)
    
    # Compute new viewport dimensions
    if width/height > target_aspect:
        # Window is wider than target - pillarbox
        new_width = int(height * target_aspect)
        glViewport((width - new_width)//2, 0, new_width, height)
    else:
        # Window is taller than target - letterbox
        new_height = int(width / target_aspect)
        glViewport(0, (height - new_height)//2, width, new_height)
    
    # Maintain original projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV_Y, target_aspect, NEAR_CLIP, FAR_CLIP)
    glMatrixMode(GL_MODELVIEW)

def idle():
    """Called by GLUT when idle. Updates animation state."""
    global earth_rotation_angle # Add this with other globals
    global earth_orbit_angle, mars_orbit_angle, jupiter_orbit_angle, saturn_orbit_angle
    global mercury_orbit_angle, venus_orbit_angle, uranus_orbit_angle, neptune_orbit_angle
    global moon_orbit_angle, phobos_orbit_angle, deimos_orbit_angle
    global io_orbit_angle, europa_orbit_angle, ganymede_orbit_angle, callisto_orbit_angle
    global titan_orbit_angle, titania_orbit_angle, triton_orbit_angle
    global asteroids
    
    # Update planet orbital angles
    earth_rotation_angle = (earth_rotation_angle + EARTH_ROTATION_SPEED * GRAVITY_FACTOR) % 360.0
    mercury_orbit_angle = (mercury_orbit_angle + MERCURY_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    venus_orbit_angle = (venus_orbit_angle + VENUS_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    earth_orbit_angle = (earth_orbit_angle + EARTH_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    mars_orbit_angle = (mars_orbit_angle + MARS_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    jupiter_orbit_angle = (jupiter_orbit_angle + JUPITER_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    saturn_orbit_angle = (saturn_orbit_angle + SATURN_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    uranus_orbit_angle = (uranus_orbit_angle + URANUS_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    neptune_orbit_angle = (neptune_orbit_angle + NEPTUNE_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    
    # Update moon orbits (also affected by gravity)
    moon_orbit_angle = (moon_orbit_angle + MOON_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    phobos_orbit_angle = (phobos_orbit_angle + PHOBOS_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    deimos_orbit_angle = (deimos_orbit_angle + DEIMOS_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    io_orbit_angle = (io_orbit_angle + IO_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    europa_orbit_angle = (europa_orbit_angle + EUROPA_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    ganymede_orbit_angle = (ganymede_orbit_angle + GANYMEDE_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    callisto_orbit_angle = (callisto_orbit_angle + CALLISTO_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    titan_orbit_angle = (titan_orbit_angle + TITAN_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    titania_orbit_angle = (titania_orbit_angle + TITANIA_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    triton_orbit_angle = (triton_orbit_angle + TRITON_ORBIT_SPEED * GRAVITY_FACTOR) % (2 * math.pi)
    
    # Update asteroid positions
    for asteroid in asteroids:
        asteroid["angle"] = (asteroid["angle"] + ASTEROID_ORBIT_SPEED * (ASTEROID_BELT_INNER_RADIUS / asteroid["distance"]) * GRAVITY_FACTOR) % (2 * math.pi)
        asteroid["x"] = asteroid["distance"] * math.cos(asteroid["angle"])
        asteroid["z"] = asteroid["distance"] * math.sin(asteroid["angle"])
    
    # Update rocket position
    update_rocket_position()
    
    # Update camera based on mode
    update_camera()
    
    glutPostRedisplay() # Request redraw

def display():
    """The main display function called by GLUT."""
    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1.0) # Black background
    
    # Set up camera and lighting for this frame
    setupCamera()
    setup_lighting() # Note: Lighting is not active without glEnable(GL_LIGHTING)
    
    # Draw scene components
    draw_starfield()
    draw_orbit_lines()
    draw_asteroid_belt()
    draw_solar_system()
    
    # Draw the rocket
    draw_rocket()
    
    # For text drawing - use fixed coordinates based on original window size
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT) # Fixed coordinates
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Update the text display to include gravity controls
    viewport = glGetIntegerv(GL_VIEWPORT)
    win_width, win_height = viewport[2], viewport[3]
    draw_text(10, win_height - 20, "Solar System Simulation - Gravity: {:.1f}x".format(GRAVITY_FACTOR))
    
    # Draw camera mode information
    draw_mode_info()
    
    # Restore previous states
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # Swap buffers to show the rendered frame
    glutSwapBuffers()

# --- Main Function ---
def main():
    """Initializes GLUT, sets up callbacks, and starts the main loop."""
    glutInit()
    
    # Request double buffering, RGB color, and depth buffer (depth buffer is requested but not enabled)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100) # Position window
    wind = glutCreateWindow(b"OpenGL Solar System - Camera Director") # Window title
    
    # Register callback functions
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    
    # Initialize scene data (stars, asteroids)
    initialize_scene()
    
    # Initialize camera director
    print("Initializing Camera Director...")
    print("Camera Controls:")
    print(" 0: Free Camera Mode")
    print(" 1: First-Person Mode (Astronaut View)")
    print(" 2: Third-Person Mode (Behind Rocket)")
    print(" 3: Crash Camera Mode")
    print(" c: Trigger Crash Sequence")
    print(" g/h: Increase/Decrease Gravity")
    print(" ,/.: Slow Down/Speed Up Earth's Rotation")
    print(" ESC: Exit")
    
    print("Starting GLUT Main Loop...")
    glutMainLoop() # Start the event processing loop

if __name__ == "__main__":
    main()

