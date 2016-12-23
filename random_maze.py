# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:42:31 2016

@author: seanm
"""
from PIL import Image
import random

#constants representing the directions/four sides of each square 

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

#global constants set when createMaze is called

HEIGHT = 0    #the adjusted height of the maze in pixels
WIDTH = 0     #the adjusted width of the maze in pixels
SIDE = 0      #the side length in pixels of each square

#constants representing the color scheme

ENTRANCE_COLOR = (0, 0, 255)
EXIT_COLOR = (255, 0, 0)
DEFAULT_COLOR = (255, 255, 255) #the background color of the maze

#class for representing the x and y coordinates of each square in the grid

class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
#returns the distance squared between two Point objects
        
def distanceSquared(start, end):
    diff_x = start.x - end.x
    diff_y = start.y - end.y
    return diff_x**2 + diff_y**2
    
#arguments: (int) height: the height in pixels of the desired maze
#           (int) width: the width in pixels of the desired maze
#           (int) side: the length in pixels of each square in the grid for the maze
#                 (this determines how wide the paths in the maze will be)
#
# "createMaze" randomly generates a maze based on the arguments given. The
# maze is saved as a jpg in the current directory
    
def createMaze(height, width, side):
    if side < 4:
        print "Grid units must be greater than or equal to 4 pixels"
        return
    image = Image.new("RGB", (width, height), "white")
    pix = image.load()
    global HEIGHT
    HEIGHT = height / side * side
    global WIDTH
    WIDTH = width / side * side
    global SIDE
    SIDE = side
    entrance = setEntrance(pix)
    exit = setExit(pix)
    image.save("maze.jpg")

    
#helper function to createMaze
#determines the entrance of the maze and colors the entrance in ENTRANCE_COLOR
#
#arguments: pix: a 2d representation of the pixels in the maze
#
#returns: a Point representing the location of the entrance on the grid 
    
def setEntrance(pix):
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
    setEdge(pix, entrance, direction, ENTRANCE_COLOR)    
    return entrance
 
   
#helper function to createMaze
#determines the exit of the maze and colors the entrance in EXIT_COLOR
#
#arguments: pix: a 2d representation of the pixels in the maze
#
#returns: a Point representing the location of the exit on the grid 

def setExit(pix):
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
    if isOccupied(pix, exit, direction):
        return setExit(pix)
    else:
        setEdge(pix, exit, direction, EXIT_COLOR)    
        return exit
            
 
#helper function to createMaze
#sets the side of the square in direction direction at location pt to the given color

#arguments:         pix: the 2d representation of the pixels in the maze
#           (Point) pt: the location of the square to color
#           (int)   direction: the side of the square to color
#           (tuple) color: rgb of the color to set the edge to 

def setEdge(pix, pt, direction, color):
    if direction == UP:
        top = (pt.y + 1) * SIDE - 1
        left = max(pt.x * SIDE - 1, 0)
        while left <= min((pt.x + 1) * SIDE, WIDTH - 1):
            pix[left, top] = color
            if top + 1 < HEIGHT:
                pix[left, top + 1] = color
            left += 1
    elif direction == DOWN:
        bottom = pt.y * SIDE
        left = max(pt.x * SIDE - 1, 0)
        while left <= min((pt.x + 1) * SIDE, WIDTH - 1):
            pix[left, bottom] = color
            if bottom - 1 >= 0:
                pix[left, bottom - 1] = color
            left += 1
    elif direction == LEFT:
        left = pt.x * SIDE
        bottom = max(pt.y * SIDE - 1, 0)
        while bottom <= min((pt.y + 1) * SIDE, HEIGHT - 1):
            pix[left, bottom] = color
            if left - 1 >= 0:
                pix[left - 1, bottom] = color
            bottom += 1
    else:
        right = (pt.x + 1) * SIDE - 1
        bottom = max(pt.y * SIDE - 1, 0)
        while bottom <= min((pt.y + 1) * SIDE, HEIGHT - 1):
            pix[right, bottom] = color
            if right + 1 < WIDTH:
                pix[right + 1, bottom] = color
            bottom += 1
            

#helper function to createMaze
#determines whether there is already an edge at the given location
#
#arguments:         pix: 2d representation of the pixels in the maze
#           (Point) pt: location of the square
#           (int)   direction: location of the side of the square
#
#returns: boolean value: True if the edge is occupied, False if it is not 
    
def isOccupied(pix, pt, direction):
    if direction == UP:
        return pix[pt.x * SIDE, (pt.y + 1) * SIDE - 1] != DEFAULT_COLOR
    elif direction == DOWN:
        return pix[pt.x * SIDE, pt.y * SIDE] != DEFAULT_COLOR
    elif direction == LEFT:
        return pix[pt.x * SIDE, pt.y * SIDE] != DEFAULT_COLOR
    else:
        return pix[(pt.x + 1) * SIDE - 1, pt.y * SIDE] != DEFAULT_COLOR
    
    