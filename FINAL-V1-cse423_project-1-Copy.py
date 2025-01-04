from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import sys
from math import cos, sin

# Global variables
car_transition_corrector_width = 30
car_transition_corrector_height = 0
widthofscreen, heightofscreen = 800, 500
gravels = []
score = 0
car_velocity_y = 0
car_upward_jump = False
start = True
tree_speed = 4
start_right=755
startleft=745
illusion=True
cloud_shifting = False
shifting_magnitude = 0

# Background state
is_winter = False  # False for sunny, True for winter
# Snowflake positions
snowflakes = [(random.uniform(0, widthofscreen), random.uniform(100, heightofscreen)) for i in range(100)]
# Example list of birds, each represented by (x_position, y_position, speed)
birds = [(random.uniform(800, 1200), random.uniform(200, 400), random.uniform(2, 5)) for i in range(3)]



# Car coordinates
c_l_l_x = 47
c_l_l_y = 100
c_u_l_x = 47
c_u_l_y = 135
c_u_r_x = 108
c_u_r_y = 135
c_l_r_x = 108
c_l_r_y = 100

# Tree coordinates
t_l_l_x, t_l_l_y = 719, 100
t_u_l_x, t_u_l_y = 719, 178
t_u_r_x, t_u_r_y = 774, 178
t_l_r_x, t_l_r_y = 774, 100

# Power coordinates
power_speed = 3
p1, p2 = 700, 100
p3, p4 = 730, 130
p5, p6 = 730, 100
p7, p8 = 760, 130
p9, p10 = 760, 100
p11, p12 = 790, 130
tree_or_power = True
game_over_printed = False
power_passed = False
tree_passed = False


# Generate gravel positions
for i in range(800):
    gravels.append((i, random.randint(92, 99)))

# Sun in the top-right corner
def draw_circle(x_center, y_center, radius, color):
    glColor3f(*color)
    
    # Initial points on the circle
    x = radius
    y = 0
    p = 1 - radius  # Decision parameter

    # Draw the 8 symmetric points of the circle
    while x >= y:
        # Draw the 8 points at all octants
        glVertex2f(x_center + x, y_center + y)
        glVertex2f(x_center - x, y_center + y)
        glVertex2f(x_center + x, y_center - y)
        glVertex2f(x_center - x, y_center - y)
        glVertex2f(x_center + y, y_center + x)
        glVertex2f(x_center - y, y_center + x)
        glVertex2f(x_center + y, y_center - x)
        glVertex2f(x_center - y, y_center - x)

        # Update the decision parameter and coordinates
        y += 1
        if p <= 0:
            p = p + 2 * y + 1  # Move vertically
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1  # Move diagonally

# Function to draw the sunny background
def draw_sunny_background():
    # Warm-toned background (sky)
    glClearColor(1.0, 0.85, 0.6, 1.0)  # Light warm yellow background
    
    # Ground (green color)
    glColor3f(0.3, 0.7, 0.3)  # Green ground
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 100)
    glVertex2f(0, 100)
    glEnd()

    # Sun (yellow circle at top-right corner)
    glBegin(GL_POINTS)
    draw_circle(650, 450, 50, (1.0, 1.0, 0.0))  # Sun in the top-right corner
    glEnd()
def draw_winter_background():
    glClearColor(0.7, 0.9, 1.0, 1.0)  # Light blue background for winter
    glColor3f(0.9, 0.9, 1.0)  # White ground for snow
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 100)
    glVertex2f(0, 100)
    glEnd()
    draw_circle(650, 450, 50, (1.0, 1.0, 0.8))  # Optional sun in the top-right corner
    draw_snowflakes()  # Draw snowflakes

def draw_snowflakes():
    glColor3f(1.0, 1.0, 1.0)  # White snowflakes
    glPointSize(4)  # Size of snowflakes
    glBegin(GL_POINTS)
    for i in range(len(snowflakes)):
        x, y = snowflakes[i]
        glVertex2f(x, y)
        # Update snowflake position
        if y > 100:  # If snowflake is above the ground (y > 100)
            y -= 1  # Move down
        else:  # If it reaches or passes the ground
            # Reset snowflake to a random position above the screen (off the top)
            x = random.uniform(0, widthofscreen)
            y = random.uniform(heightofscreen, heightofscreen + 50)
        
        snowflakes[i] = (x, y)  # Update the position
    glEnd()
def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = abs(dy) > abs(dx)
   
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx
   
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
   
    d = 2 * dy - dx
    y = y1
   
    for x in range(int(x1), int(x2) + 1):
        if steep:
            glBegin(GL_POINTS)
            glVertex2f(int(y), int(x))
            glEnd()
        else:
            glBegin(GL_POINTS)
            glVertex2f(int(x), int(y))
            glEnd()
       
        if d > 0:
            y += 1 if y1 < y2 else -1
            d -= 2 * dx
        d += 2 * dy

def ground():
    glColor3f(1, 1, 1)  # White ground for both backgrounds
    draw_line(0, 100, 800, 100, (1, 1, 1))
    for i in gravels:
        glBegin(GL_POINTS)
        glVertex2f(i[0], i[1])
        glEnd()
def circle_points(x, y, cx, cy):
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)

    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)

    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)

    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)


def mid_circle(cx, cy, radius):
    d = 1 - radius
    x = 0
    y = radius
    circle_points(x, y, cx, cy)
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y = y - 1
        x = x + 1
        circle_points(x, y, cx, cy)

def draw_bird(x, y):
    glColor3f(0.0, 0.0, 0.0)  # Set the bird color to black (0.0, 0.0, 0.0)
    glPointSize(2)
    
    # Body and wings using lines
    # Left wing upper part
    draw_line(x - 10, y + 5, x - 15, y + 10, (0.0, 0.0, 0.0))  # Wing in black
    # Left wing lower part
    draw_line(x - 10, y + 5, x - 5, y + 10, (0.0, 0.0, 0.0))  # Wing in black
    
    # Right wing upper part
    draw_line(x + 10, y + 5, x + 15, y + 10, (0.0, 0.0, 0.0))  # Wing in black
    # Right wing lower part
    draw_line(x + 10, y + 5, x + 5, y + 10, (0.0, 0.0, 0.0))  # Wing in black

    # Draw the body of the bird
    glBegin(GL_QUADS)
    for i in range(360):
        angle = 2 * 3.14159 * i / 360
        dx = 10 * cos(angle)  # Radius of the bird's body
        dy = 5 * sin(angle)   # Radius of the bird's body
        glVertex2f(x + dx, y + dy)  # Vertex for each point on the body
    glEnd()


def update_birds():
    global birds
    for i in range(len(birds)):
        x, y, speed = birds[i]
        x -= speed  # Move the bird leftward (speed controls the speed of flight)
        
        # If the bird flies off-screen, reset it to a random position on the right side
        if x < -20:  # Bird is off-screen on the left
            x = random.uniform(800, 1200)  # New random x position for the bird
            y = random.uniform(200, 400)   # Randomize the y position as well
        
        birds[i] = (x, y, speed)  # Update bird's position and speed
  

def vehicle():
    global car_transition_corrector_width, car_transition_corrector_height
    draw_line(20 + car_transition_corrector_width, 110 + car_transition_corrector_height, 75 + car_transition_corrector_width, 110 + car_transition_corrector_height, (1, 1, 1))  # Bottom line
    draw_line(20 + car_transition_corrector_width, 110 + car_transition_corrector_height, 20 + car_transition_corrector_width, 120 + car_transition_corrector_height, (1, 1, 1))  # Left vertical line
    draw_line(75 + car_transition_corrector_width, 110 + car_transition_corrector_height, 75 + car_transition_corrector_width, 120 + car_transition_corrector_height, (1, 1, 1))  # Right vertical line
    draw_line(20 + car_transition_corrector_width, 120 + car_transition_corrector_height, 30 + car_transition_corrector_width, 120 + car_transition_corrector_height, (1, 1, 1))  # Left top line
    draw_line(30 + car_transition_corrector_width, 120 + car_transition_corrector_height, 30 + car_transition_corrector_width, 130 + car_transition_corrector_height, (1, 1, 1))  # Right top line
    draw_line(75 + car_transition_corrector_width, 120 + car_transition_corrector_height, 65 + car_transition_corrector_width, 120 + car_transition_corrector_height, (1, 1, 1))  # Right top line to left
    draw_line(65 + car_transition_corrector_width, 120 + car_transition_corrector_height, 65 + car_transition_corrector_width, 130 + car_transition_corrector_height, (1, 1, 1))  # Left top line
    draw_line(30 + car_transition_corrector_width, 130 + car_transition_corrector_height, 65 + car_transition_corrector_width, 130 + car_transition_corrector_height, (1, 1, 1))  # Head

    draw_line(c_l_l_x, c_l_l_y, c_u_l_x, c_u_l_y, (0, 0, 0))
    draw_line(c_u_l_x, c_u_l_y, c_u_r_x, c_u_r_y, (0, 0, 0))
    draw_line(c_l_r_x, c_l_r_y, c_u_r_x, c_u_r_y, (0, 0, 0))
    draw_line(c_l_r_x, c_l_r_y, c_l_l_x, c_l_l_y, (0, 0, 0))

def trees():
    global tree_or_power
    if tree_or_power==True:
        global tree_speed
        glEnable(GL_POINT_SMOOTH)
        for i in range(755-tree_speed,745-tree_speed,-1):
            draw_line(i,100,i,130,(165/255, 42/255, 42/255))
        #tree

        draw_line(t_u_l_x,t_u_l_y,t_l_l_x,t_l_l_y,(1,1,1))
        draw_line(t_l_r_x,t_l_r_y,t_u_r_x,t_u_r_y,(1,1,1))
        draw_line(t_u_l_x,t_u_l_y,t_u_r_x,t_u_r_y,(1,1,1))
        draw_line(t_l_l_x,t_l_l_y,t_l_r_x,t_l_r_y,(1,1,1))
        # draw_line
        glColor3f(0, 1, 0)
        glPointSize(20)
        glBegin(GL_POINTS)
        glVertex2f(750-tree_speed,140)
        glVertex2f(735-tree_speed,145)
        glVertex2f(765-tree_speed,145)
        glVertex2f(750-tree_speed,150)
        glVertex2f(750-tree_speed,166)

        glEnd()


    # Drawing lines with updated coordinates
    else:
        glPointSize(3)
        glColor3f(0.5, 0.5, 0.5)  # color for the power box
        draw_line(p1, p2, p1, p4, (0.5, 0.5, 0.5))  # Left edge
        draw_line(p1, p4, p3, p4, (0.5, 0.5, 0.5))  # Top edge
        draw_line(p3, p4, p3, p2, (0.5, 0.5, 0.5))  # Right edge
        draw_line(p3, p2, p1, p2, (0.5, 0.5, 0.5))  # Bottom edge
def clouds():
    glEnable(GL_POINT_SMOOTH)
    glColor3f(0.7, 0.7, 0.7)  # Set color to ash white
    glPointSize(20)
    glBegin(GL_POINTS)

    # First cloud (up)
    glVertex2f(100, 450)  # High position
    glVertex2f(120, 450)
    glVertex2f(140, 450)
    glVertex2f(110, 460)
    glVertex2f(130, 460)

    # Second cloud (slightly down)
    glVertex2f(200, 440)  # Slightly lower
    glVertex2f(220, 440)
    glVertex2f(240, 440)
    glVertex2f(210, 450)
    glVertex2f(230, 450)

    # Third cloud (more down)
    glVertex2f(300, 430)  # More down
    glVertex2f(320, 430)
    glVertex2f(340, 430)
    glVertex2f(310, 440)
    glVertex2f(330, 440)

    # Fourth cloud (more up)
    glVertex2f(400, 450)  # Back up
    glVertex2f(420, 450)
    glVertex2f(440, 450)
    glVertex2f(410, 460)
    glVertex2f(430, 460)

    # Fifth cloud (little right up)
    glVertex2f(500, 440)  # Slightly to the right and up
    glVertex2f(520, 440)
    glVertex2f(540, 440)
    glVertex2f(510, 450)
    glVertex2f(530, 450)

    glEnd()

def update():
    global tree_speed, shifting_magnitude
    global t_l_l_x, t_u_l_x, t_u_r_x, t_l_r_x, t_u_r_y
    global c_l_l_x, c_l_l_y, c_l_r_x, c_l_r_y, c_u_l_x, c_u_l_y, c_u_r_x, c_u_r_y
    global score, start, tree_or_power
    global power_speed, p1, p2, p3, p4

    #new
    global game_over_printed
    global power_passed, tree_passed
    if tree_or_power:  # Logic for tree
        if start:
            if tree_speed >= 750:
                tree_speed = 4
                t_l_l_x, t_l_l_y = 719, 100
                t_u_l_x, t_u_l_y = 719, 178
                t_u_r_x, t_u_r_y = 774, 178
                t_l_r_x, t_l_r_y = 774, 100
                tree_or_power = not tree_or_power
            tree_speed += 4
            t_l_l_x -= 4
            t_u_l_x -= 4
            t_u_r_x -= 4
            t_l_r_x -= 4
            if ((c_l_l_x <= t_l_l_x <= c_l_r_x) or (c_l_l_x <= t_l_r_x <= c_l_r_x)) and (c_l_r_y >= t_u_r_y):
                if not tree_passed:  # Only increment score once after avoiding the tree
                    score += 2  # Increase score by 2 when avoiding the tree
                    print(f"Score: {score}")  # Display score each time it increases
                    tree_passed = True  # Mark the tree as passed without collision

            elif ((c_l_l_x <= t_l_l_x <= c_l_r_x) or (c_l_l_x <= t_l_r_x <= c_l_r_x)) and (c_l_r_y <= t_u_r_y):
                if not game_over_printed:  # Check if the game over message has already been printed
                    print("game over")
                    game_over_printed = True  # Set the flag to True to prevent printing again
                start = False  # Stop the game

    else:  # Logic for power box
        if start:
            # Update x-coordinates for horizontal movement
            p1 -= power_speed
            p3 -= power_speed

        # Calculate the edges of the power box
        power_left = p1
        power_right = p3
        power_top = p4
        power_bottom = p2

        # Check for collision between the power box and the player's bounding box
        # Player's bounding box
        player_left = c_l_l_x
        player_right = c_l_r_x
        player_top = c_u_l_y
        player_bottom = c_l_r_y

        # Check if the bounding boxes intersect (collision detection)
        if (power_left < player_right and power_right > player_left and
            power_top > player_bottom and power_bottom < player_top):
            if not game_over_printed:  # Check if the game over message has already been printed
                print("game over")
                game_over_printed = True  # Set the flag to True to prevent printing again
            start = False  # Stop the game
            power_passed = False  # Mark the power rectangle as not passed

        else:
            # Only increment score after the car successfully avoids the power box (rectangle) by jumping
            if not power_passed:  # Only increment score once after passing power box
                score += 1
                print(f"Score: {score}")  # Display score each time it increases

                power_passed = True  # Mark the power box as passed without collision

        # Reset power box position if it moves off-screen
        if p3 < 0 or p1 < 0:
            p1 = 700
            p2 = 100
            p3 = 740
            p4 = 140
            tree_or_power = not tree_or_power
            power_passed = False  # Reset the flag when the power box resets
            tree_passed = False  # Reset the flag when the tree resets

def display():
    global car_transition_corrector_width, car_transition_corrector_height, car_velocity_y, car_upward_jump,c_l_l_y,c_u_l_y,c_u_r_y,c_l_r_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.447, 1.0, 0.973)
    glPointSize(1)
    glBegin(GL_POINTS)
    for i in range(5):
        mid_circle(35+car_transition_corrector_width, 106+car_transition_corrector_height, i)
        mid_circle(60+car_transition_corrector_width,106+car_transition_corrector_height,i)

    glEnd()
    if car_upward_jump:
        car_transition_corrector_height += car_velocity_y
        c_l_l_y+=car_velocity_y
        c_u_l_y+=car_velocity_y
        c_u_r_y+=car_velocity_y
        c_l_r_y+=car_velocity_y
        car_velocity_y -= 0.2  # Adjust the gravity effect as needed

        if car_transition_corrector_height <= 0:
            car_transition_corrector_height = 0
            car_upward_jump = False
            car_velocity_y = 0
    if is_winter:
        draw_winter_background()
    else:
        draw_sunny_background()
    ground()
    vehicle()
    trees()
    clouds()
    for i in birds:
        draw_bird(i[0], i[1])  # Draw each bird at its current position
    
    update_birds()  # Update the positions of the birds
    
    update()
    glutSwapBuffers()

def keyboard(key, x, y):
    global car_transition_corrector_height, car_velocity_y, car_upward_jump, is_winter
    if key == b' ' and not car_upward_jump:
        car_upward_jump = True
        car_velocity_y = 9  # Adjust the jump height as needed
    elif key == b'm':  # Switch to morning (sunny)
        is_winter = False
    elif key == b'n':  # Switch to night (winter)
        is_winter = True

def animation():
    time = glutGet(GLUT_ELAPSED_TIME) / 1000.0  # Convert milliseconds to seconds
    glutPostRedisplay()

# OpenGL initialization
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(widthofscreen, heightofscreen)
glutCreateWindow(b"Project")
glOrtho(0, widthofscreen, 0, heightofscreen, -1, 1)
glClearColor(0, 0, 0, 1)

# Register callbacks
glutKeyboardFunc(keyboard)
glutDisplayFunc(display)
glutIdleFunc(animation)

# Start the main loop
glutMainLoop()
opengl.gl