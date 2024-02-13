from OpenGL.GL import *
from OpenGL.GLUT import *
import math

w_wid = 600
w_hgt = 600
bub_rad = 15
fball_rad = 30
c_speed = 0.3


gpost_wid = w_wid * 0.3
score=0

circles = []
fball_pos = {"x": w_wid / 2, "y": fball_rad, "rad": fball_rad, "color": (1.0, 1.0, 1.0)}
# gpost_wid = 50


# bubble
def draw_circle(cen_x, cen_y, rad, color): 
    glBegin(GL_POINTS)
    glColor3f(*color)
    d = 1 - rad
    x = 0
    y = rad
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        glVertex2f(x + cen_x, y + cen_y)
        glVertex2f(y + cen_x, x + cen_y)
        glVertex2f(-x + cen_x, y + cen_y)
        glVertex2f(-y + cen_x, x + cen_y)
        glVertex2f(-x + cen_x, -y + cen_y)
        glVertex2f(-y + cen_x, -x + cen_y)
        glVertex2f(x + cen_x, -y + cen_y)
        glVertex2f(y + cen_x, -x + cen_y)
    glEnd()

# goalpost
def draw_gpost():
    gpost_wid = w_wid * 0.3  
    goalpost_height = w_hgt * 0.6  

    glColor3f(1.0, 1.0, 1.0)  
    glBegin(GL_QUADS)
    glVertex2f(w_wid / 2 - gpost_wid / 2, w_hgt - bub_rad * 2)
    glVertex2f(w_wid / 2 - gpost_wid / 2, w_hgt + goalpost_height)
    glVertex2f(w_wid / 2 + gpost_wid / 2, w_hgt + goalpost_height)
    glVertex2f(w_wid / 2 + gpost_wid / 2, w_hgt - bub_rad * 2)
    glEnd()



fball_pos = [w_wid / 2, fball_rad]

def draw_fball():
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(fball_pos[0], fball_pos[1])

    number_segments = 100
    for i in range(number_segments + 1):
        angle = math.pi * 2.0 * i / number_segments
        x = fball_pos[0] + fball_pos[2] * math.cos(angle)
        y = fball_pos[1] + fball_pos[2] * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

def draw_objects():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    for circle in circles:
        draw_circle(circle['x'], circle['y'], circle['rad'], circle['color'])
    draw_gpost()
    draw_fball()

def move_bubbles():
    for circle in circles:
        circle['x'] += circle['speed_x']
        circle['y'] += circle['speed_y']

        if circle['x'] + circle['rad'] > w_wid or circle['x'] - circle['rad'] < 0:
            circle['speed_x'] *= -1
        if circle['y'] + circle['rad'] > w_hgt or circle['y'] - circle['rad'] < 0:
            circle['speed_y'] *= -1

keys = {'w': False, 's': False, 'a': False, 'd': False}

fball_velocity = [0, 0]

fball_pos = [w_wid / 2, fball_rad, fball_rad]

def move_football():
    global fball_velocity

    speed = 2 
    diagonal_speed = speed * math.cos(math.radians(45))  
    if keys['w']:
        fball_velocity = [0, speed]
    elif keys['s']:
        fball_velocity[1] = -speed
    if keys['a']:
        fball_velocity[0] = -diagonal_speed
        fball_velocity[1] = diagonal_speed
    elif keys['d']:
        fball_velocity[0] = diagonal_speed
        fball_velocity[1] = diagonal_speed
    
    fball_pos[0] += fball_velocity[0]
    fball_pos[1] += fball_velocity[1]


    if fball_pos[0] + fball_pos[2] > w_wid:
        fball_velocity[0] *= -1
        fball_pos[0] = w_wid - fball_pos[2]
    elif fball_pos[0] - fball_pos[2] < 0:
        fball_velocity[0] *= -1
        fball_pos[0] = fball_pos[2]

    if fball_pos[1] + fball_pos[2] > w_hgt:
        fball_velocity[1] *= -1
        fball_pos[1] = w_hgt - fball_pos[2]
    elif fball_pos[1] - fball_pos[2] < 0:
        fball_velocity[1] *= -1
        fball_pos[1] = fball_pos[2]

    check_collision()


def check_collision():
    global fball_velocity


    for circle in circles:
        dist = math.sqrt((fball_pos[0] - circle['x'])**2 + (fball_pos[1] - circle['y'])**2)
        if dist < fball_pos[2] + circle['rad']:
            
            dx = fball_pos[0] - circle['x']
            dy = fball_pos[1] - circle['y']
            angle = math.atan2(dy, dx)
            fball_velocity = [math.cos(angle), math.sin(angle)]
            


def keyboard_press(key, x, y):
    global score
    key = key.decode('utf-8').lower()
    if key in keys:
        keys[key] = True
    elif key == 'r':
        score = 0  
        reset_position()  

def keyboard_release(key, x, y):
    key = key.decode('utf-8').lower()
    if key in keys:
        keys[key] = False
        
        
def check_goal():
        global score
        gpost_top = w_hgt + bub_rad
        gpost_bottom = w_hgt - bub_rad * 2

        if gpost_bottom <= fball_pos[1] + fball_pos[2] <= gpost_top:
            if w_wid / 2 - gpost_wid / 2 <= fball_pos[0] <= w_wid / 2 + gpost_wid / 2:

                score += 1
                print(f"Goal! Score: {score}")
                reset_position()
                
def reset_position():
    global fball_pos, score, fball_rad

    fball_pos[0] = 600/ 2
    fball_pos[1] = fball_rad
               

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(2)

    move_bubbles()
    draw_objects()

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, w_wid, 0, w_hgt, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1.0, 1.0, 1.0) 

    
    if 0 <= score < 10:
        glRasterPos2f(20, w_hgt - 20)
        score_text = f"Score: {score}"
    else:
        glRasterPos2f(300, w_hgt - 300)
        score_text = "You win the game"

        
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glutSwapBuffers()

    check_goal()
    if score <= -10:
        print("Game Over! You reached a score of -10 or higher.")
    elif score >= 10:      
        print("You win the game")

    move_football()
    glutPostRedisplay()    


def main():
    for i in range(13):
        circles.append({"x": w_wid / 2, "y": w_hgt / 2, "rad": bub_rad, "color": (0.447, 1.0, 0.973),
                        "speed_x": c_speed * math.cos(math.radians(i * 27.6923)),
                        "speed_y": c_speed * math.sin(math.radians(i * 27.6923))})
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(w_wid, w_hgt)
    glutCreateWindow(b"Football Game")
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w_wid, 0, w_hgt, -1, 1)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_press)
    glutKeyboardUpFunc(keyboard_release)    
    glutMainLoop()

if __name__ == "__main__":
    main()