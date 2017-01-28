# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:42:31 2016

@author: seanm
"""
from PIL import Image
import random
import math
import Queue

#constants representing the directions/four sides of each square 

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

#global constants set when create_maze is called

HEIGHT = 0    #the adjusted height of the maze in pixels
WIDTH = 0     #the adjusted width of the maze in pixels
SIDE = 0      #the side length in pixels of each square

#constants representing the color scheme (THESE MUST BE DIFFERENT FROM EACH OTHER)

ENTRANCE_COLOR = (0, 0, 255)
EXIT_COLOR = (255, 0, 0)
DEFAULT_COLOR = (255, 255, 255) #the background color of the maze
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (0, 1, 0)

#constants for determining guarantteed path

SAME_DIR_MULT = 3
DIST_MULT = 2

#constants for probability of adding edges 

SUCCESS = 9
BASE_LINE = 270
DIVIDER = 3

#class for representing the x and y coordinates of each square in the grid

class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)
    
    def __ne__(self, other):
        return (self.x != other.x or self.y != other.y)
        
    def __cmp__(self, other):
        return self.x + self.y - other.x - other.y
        
    def __hash__(self):
        return self.x * self.y
 
       
#returns the distance squared between two Point objects
        
def distance_squared(start, end):
    diff_x = start.x - end.x
    diff_y = start.y - end.y
    return diff_x**2 + diff_y**2
 
   
#arguments: (int) height: the height in grid squares of the desired maze
#           (int) width: the width in grid squares of the desired maze
#           (int) side: the length in pixels of each square in the grid for the maze
#                 (this determines how wide the paths in the maze will be)
#
# "create_maze" randomly generates a maze based on the arguments given. The
# maze is saved as a jpg in the current directory
    
def create_maze(height, width, side):
    if side < 4:
        print "Grid units must be greater than or equal to 4 pixels"
        return
    global HEIGHT
    HEIGHT = height * side
    global WIDTH
    WIDTH = width * side
    global SIDE
    SIDE = side
    image = Image.new("RGB", (WIDTH, HEIGHT), "#ffffff")
    pix = image.load()
    entrance = set_entrance(pix)
    exit = set_exit(pix)
    set_boundaries(pix)
    add_walls(pix, entrance, exit)
    image.save("maze.jpg")

    
#helper function to create_maze
#determines the entrance of the maze and colors the entrance in ENTRANCE_COLOR
#
#arguments: pix: a 2d representation of the pixels in the maze
#
#returns: a Point representing the location of the entrance on the grid 
    
def set_entrance(pix):
    direction = random.randint(0,3)
    if direction == UP:
        place = random.randint(0, WIDTH / SIDE - 1)
        entrance = Point(place, HEIGHT / SIDE - 1)
    elif direction == DOWN:
        place = random.randint(0, WIDTH / SIDE - 1)
        entrance = Point(place, 0)
    elif direction == LEFT:
        place = random.randint(0, HEIGHT / SIDE - 1)
        entrance = Point(0, place)
    else:
        place = random.randint(0, HEIGHT / SIDE - 1)
        entrance = Point(WIDTH / SIDE - 1, place)
    set_square(pix, entrance, direction, ENTRANCE_COLOR)    
    return entrance
 
   
#helper function to create_maze
#determines the exit of the maze and colors the entrance in EXIT_COLOR
#
#arguments: pix: a 2d representation of the pixels in the maze
#
#returns: a Point representing the location of the exit on the grid 

def set_exit(pix):
    direction = random.randint(0, 3)
    if direction == UP:
        place = random.randint(0, WIDTH / SIDE - 1)
        exit = Point(place, HEIGHT / SIDE - 1)
    elif direction == DOWN:
        place = random.randint(0, WIDTH / SIDE - 1)
        exit = Point(place, 0)
    elif direction == LEFT:
        place = random.randint(0, HEIGHT / SIDE - 1)
        exit = Point(0, place)
    else:
        place = random.randint(0, HEIGHT / SIDE - 1)
        exit = Point(WIDTH / SIDE - 1, place)
    if is_occupied(pix, exit, direction):
        return set_exit(pix)
    else:
        set_square(pix, exit, direction, EXIT_COLOR)    
        return exit


#helper function for create_maze
#puts edges at the boundaries of the maze
#
#arguments: pix: a 2d representation of the pixels in the maze        

def set_boundaries(pix):
    for i in range(HEIGHT / SIDE):
        pt = Point(0, i)
        if not is_occupied(pix, pt, LEFT):
            set_edge(pix, pt, LEFT, WALL_COLOR)
        pt = Point(WIDTH / SIDE - 1, i)
        if not is_occupied(pix, pt, RIGHT):
            set_edge(pix, pt, RIGHT, WALL_COLOR)
    for i in range(WIDTH / SIDE):
        pt = Point(i, 0)
        if not is_occupied(pix, pt, DOWN):
            set_edge(pix, pt, DOWN, WALL_COLOR)
        pt = Point(i, HEIGHT / SIDE - 1)
        if not is_occupied(pix, pt, UP):
            set_edge(pix, pt, UP, WALL_COLOR)

   
#helper function for create_maze
#iterates through each square in the grid and adds edges at random
#before adding an edge, it checks to see if the maze is still solvable
   
#arguments: pix: 2d representation of the pixels of the maze
     
def add_walls(pix, start, end):
    width = WIDTH / SIDE
    height = HEIGHT / SIDE
    for i in range(width):
        for j in range(height):
            pt = Point(i, j)
            options = []
            for a in range(4):
                if not is_occupied(pix, pt, a):
                    options.append(a)
            for b in range(len(options)):
                choice = random.randint(1, BASE_LINE / DIVIDER**b)
                if choice <= SUCCESS:
                    choice2 = random.randint(0, len(options) - 1)
                    set_edge(pix, pt, options[choice2], WALL_COLOR)
                    if not is_connected(pix, start, end):
                        set_edge(pix, pt, options[choice2], DEFAULT_COLOR)
                    del options[choice2]
                        
 
#helper function to create_maze
#sets the side of the square in direction direction at location pt to the given color

#arguments:         pix: the 2d representation of the pixels in the maze
#           (Point) pt: the location of the square to color
#           (int)   direction: the side of the square to color
#           (tuple) color: rgb of the color to set the edge to 

def set_edge(pix, pt, direction, color):
    if direction == UP:
        top = (pt.y + 1) * SIDE - 1
        left = pt.x * SIDE
        while left < (pt.x + 1) * SIDE:
            pix[left, top] = color
            if top + 1 < HEIGHT:
                pix[left, top + 1] = color
            left += 1
    elif direction == DOWN:
        bottom = pt.y * SIDE
        left = pt.x * SIDE
        while left < (pt.x + 1) * SIDE:
            pix[left, bottom] = color
            if bottom - 1 >= 0:
                pix[left, bottom - 1] = color
            left += 1
    elif direction == LEFT:
        left = pt.x * SIDE
        bottom = pt.y * SIDE
        while bottom < (pt.y + 1) * SIDE:
            pix[left, bottom] = color
            if left - 1 >= 0:
                pix[left - 1, bottom] = color
            bottom += 1
    else:
        right = (pt.x + 1) * SIDE - 1
        bottom = pt.y * SIDE
        while bottom < (pt.y + 1) * SIDE:
            pix[right, bottom] = color
            if right + 1 < WIDTH:
                pix[right + 1, bottom] = color
            bottom += 1
 

#helper function for create_maze
#sets an edge and colors in the entire square (except for the other edges)

#arguments:        pix: 2d pixel representaiton of the maze
#          (Point) pt: the square to be colored in
#          (int)   direction: indicates the edge to be colored in
#          (tuple) color: the rgb color the square should be

def set_square(pix, pt, direction, color):
    if direction == UP:
        top = (pt.y + 1) * SIDE - 2
        left = pt.x * SIDE + 1
        while left <= (pt.x + 1) * SIDE - 2:
            top2 = top
            while top2 > pt.y * SIDE:
                pix[left, top2] = color
                top2 -= 1
            left += 1
    elif direction == DOWN:
        bottom = pt.y * SIDE + 1
        left = pt.x * SIDE + 1
        while left <= (pt.x + 1) * SIDE - 2:
            bottom2 = bottom
            while bottom2 < (pt.y + 1) * SIDE - 1:
                pix[left, bottom2] = color
                bottom2 += 1
            left += 1
    elif direction == LEFT:
        left = pt.x * SIDE + 1
        bottom = pt.y * SIDE + 1
        while bottom <= (pt.y + 1) * SIDE - 2:
            left2 = left
            while left2 < (pt.x + 1) * SIDE - 1:
                pix[left2, bottom] = color
                left2 += 1
            bottom += 1
    else:
        right = (pt.x + 1) * SIDE - 2
        bottom = pt.y * SIDE + 1
        while bottom <= (pt.y + 1) * SIDE - 2:
            right2 = right
            while right2 > pt.x * SIDE:
                pix[right2, bottom] = color
                right2 -= 1
            bottom += 1               


#helper function to create_maze
#determines whether there is already an edge at the given location
#
#arguments:         pix: 2d representation of the pixels in the maze
#           (Point) pt: location of the square
#           (int)   direction: location of the side of the square
#
#returns: boolean value: True if the edge is occupied, False if it is not 
    
def is_occupied(pix, pt, direction):
    if direction == UP:
        return pix[pt.x * SIDE + 2, (pt.y + 1) * SIDE - 1] != DEFAULT_COLOR
    elif direction == DOWN:
        return pix[pt.x * SIDE + 2, pt.y * SIDE] != DEFAULT_COLOR
    elif direction == LEFT:
        return pix[pt.x * SIDE, pt.y * SIDE + 2] != DEFAULT_COLOR
    else:
        return pix[(pt.x + 1) * SIDE - 1, pt.y * SIDE + 2] != DEFAULT_COLOR
   

#helper function for create_maze
#returns the coordinates of the square one away from pt in the given direction
     
def next_pt(pt, direction):
    if direction == UP:
        return Point(pt.x, pt.y + 1)
    elif direction == DOWN:
        return Point(pt.x, pt.y - 1)
    elif direction == LEFT:
        return Point(pt.x - 1, pt.y)
    else:
        return Point(pt.x + 1, pt.y)


#helper function for create_maze
#returns true if a path from Point start to Point end exists
#returns false otherwise

def is_connected(pix, start, end):
    a = 0
    lst = Queue.PriorityQueue()
    st = set()
    st.add(start)
    for i in range(4):
        if not is_occupied(pix, start, i):
            nxt = next_pt(start, i)
            lst.put((distance_squared(nxt, end), nxt))
            st.add(nxt)
    while not lst.empty():
        loc = lst.get()[1]
        if loc == end:
            return True     
        for i in range(4):
            nxt = next_pt(loc, i)
            if not is_occupied(pix, loc, i) and nxt not in st:
                lst.put((distance_squared(nxt, end), nxt))
                st.add(nxt)
        a +=1
    return False

    
    