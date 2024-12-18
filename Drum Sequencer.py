"""
Name: Primo Moreno
CSC 201
Project 2-Drum Sequencer

This program lets the user build and play drum rhythms like the classic Roland TR-808.
Rows of buttons can be toggled to determine when to play samples at each step in the pattern.

Document Assistance: (who and what  OR  declare that you gave or received no assistance):
I have some previous coding experience with dictionaries, which I used to create the buttons and store values throughout the program.
I followed this link to refresh what I knew about the data type. https://www.w3schools.com/python/python_dictionaries.asp


"""

import math
import time

from graphics2 import *
from sounds import *

TRACKLENGTH = 16
BUTTONSIZE = 15
INITIALTEMPO = 120


def isPointOnButton(point, button):
    """
    The function computes the distance between a clicked
    point and the center of a circular button
    
    Parameters:
    point (Point): a point with x, y coordinates
    button (Circle): a Circle object used as a button
    
    Returns:
    bool: whether the point is in the button
    """
    x1 = point.getX()
    y1 = point.getY()
    x2 = button.getCenter().getX()
    y2 = button.getCenter().getY()
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance < button.getRadius()

def create_labels(window):
    '''
    This function creates and draws the labels for the 4 row of buttons
    and the word tempo in window in there respective places.
    
    Parameters:
    window (GraphWin): The variable name of the window
    '''
    kick_lab = Text(Point(60, 150), "Kick")
    snare_lab = Text(Point(60, 200), "Snare")
    HiHat_closed_lab = Text(Point(60, 250), "HiHat Closed")
    HiHat_open_lab = Text(Point(60, 300), "HiHat Open")
    
    kick_lab.draw(window)
    snare_lab.draw(window)
    HiHat_open_lab.draw(window)
    HiHat_closed_lab.draw(window)

def create_tempo_box_label(window):
    '''
    This function creates and draws the tempo label and input box that corresponds to the play tempo
    
    Parameters:
    window (GraphWin): The variable name of the window
    '''
    tempo_label = Text(Point(330, 60), "Tempo:")
    tempo_label.draw(window)
    
    tempo_entry = Entry(Point(400, 60), 5)
    tempo_entry.setTextColor("Black")
    tempo_entry.setText(INITIALTEMPO)
    tempo_entry.draw(window)
    
    return tempo_entry

def create_colored_buttons(window, TRACKLENGTH, BUTTONSIZE):
    '''
    The function loops through 2 for loops to create values i and j that are used when creating the names for the circles
    i delineates the row the button is in and j relates to the circle's column
    During the looping the x_val and y_val are changed to provide the correct spacing an position for each circle
    Every time a new circle is created it is added to a dictionary that stores the button with a unique name regarding it's column and row
    and the circle's properties.
    
    Parameters:
    window (GraphWin): The variable name of the window
    TRACKLENGTH: The constant for how long the track should be
    BUTTONSIZE: The constant for what size the buttons should be
    
    Returns:
    dict: the dictionary that holds the names and values of all the buttons 
    '''
    button_dict = {}
    
    x_val = 110
    y_val = 100
    for i in range(4):
        y_val += 50
        x_val = 110
        for j in range(TRACKLENGTH):
            x_val += 50
            button_dict[f'button_{i + 1}_{j + 1}'] = Circle(Point(x_val, y_val), BUTTONSIZE)
    
    for button in button_dict:
        button_dict[f'{button}'].setFill("Red")
        button_dict[f'{button}'].draw(window)
    return button_dict

def create_start_stop_button(window):
    '''
    This function creates and draws the start and stop buttons in the window for the beat sequencer
    
    Parameters:
    window (GraphWin): The variable name of the window
    
    Returns:
    shape: the circle related to the start button
    shape: the circle related to the stop button
    '''
    black_play_button = Circle(Point(100, 60), BUTTONSIZE * 2 + 2)
    black_play_button.setFill("Black")
    black_play_button.draw(window)
    
    play_button = Circle(Point(100, 60), BUTTONSIZE * 2)
    play_button.setFill("Blue")
    play_button.draw(window)
    
    start_triangle = Polygon(Point(88, 45), Point(88, 75), Point(118, 60))
    start_triangle.setFill("Cyan")
    start_triangle.draw(window)
    
    black_stop_button = Circle(Point(200, 60), BUTTONSIZE * 2 + 2)
    black_stop_button.setFill("Black")
    black_stop_button.draw(window)
    
    stop_button = Circle(Point(200, 60), BUTTONSIZE * 2)
    stop_button.setFill("Blue")
    stop_button.draw(window)
    
    stop_square = Rectangle(Point(185, 45), Point(215, 75))
    stop_square.setFill("Cyan")
    stop_square.draw(window)
    
    return (play_button, stop_button)
                           
def create_black_circles(window):
    '''
    This function creates the black outline to the colored buttons in the beat sequencer
    
    Parameters:
    window (GraphWin): The variable name of the window
    
    Returns:
    dictionary: Dictionary of the black circles outlining the colored circles
    '''
    black_button_dict = {}
    
    x_val = 110
    y_val = 100
    for j in range(16):
        x_val += 50
        y_val = 100
        for i in range(4):
            y_val += 50
            black_button_dict[f'button_{i + 1}_{j + 1}'] = Circle(Point(x_val, y_val), BUTTONSIZE + 4)
                                
    for button in black_button_dict:
        black_button_dict[f'{button}'].setFill("Black")
        black_button_dict[f'{button}'].draw(window)
    
    return black_button_dict

def change_red_to_green(window, point, red_vals, red_button_dict, button_dict, light_green):
    '''
    Parameters:
    window (GraphWin): The variable name of the window
    point: the x and y values of the last place the user clicked on the screen
    red_vals: the circle value of all the red circles
    red_button_dict: the dictionary that holds all the names and values for the red circles
    button_dict: the dictionary that holds the names and values of all the buttons
    light_green: an RGB defined color for the green circles
    
    Returns:
    list: a list containing the value and the name of the circle that had it's color changed
    '''
    for red in red_vals:
        if isPointOnButton(point, red) == True:
            name = list(red_button_dict.keys())[red_vals.index(red)]
            button_dict[name].setFill(light_green)
            values = [red, name]
            return values

def change_green_to_red(window, point, green_vals, green_button_dict, button_dict):
    '''
    Parameters:
    window (GraphWin): The variable name of the window
    point: the x and y values of the last place the user clicked on the screen
    green_vals: the circle value of all the green circles
    green_button_dict: the dictionary that holds all the names and values for the green circles
    button_dict: the dictionary that holds the names and values of all the buttons
    
    Returns:
    list: a list containing the value and the name of the circle that had it's color changed
    '''
    for green in green_vals:    
        if isPointOnButton(point, green) == True:
            name = list(green_button_dict.keys())[green_vals.index(green)]
            button_dict[name].setFill("Red")
            values = [green, name]
            return values

def change_off_buttons_on(window, point, red_vals, red_button_dict, green_button_dict, button_dict, light_green):
    '''
    Parameters:
    window (GraphWin): The variable name of the window
    point: the x and y values of the last place the user clicked on the screen
    red_vals: the circle value of all the red circles
    red_button_dict: the dictionary that holds all the names and values for the red circles
    green_button_dict: the dictionary that holds all the names and values for the green circles
    button_dict: the dictionary that holds the names and values of all the buttons
    light_green: an RGB defined color for the green circles
    
    Returns:
    dictionary: Dictionary of the red circles
    dictionary: Dictionary of the green circles
    '''
    values = change_red_to_green(window, point, red_vals, red_button_dict, button_dict, light_green)
    green_button_dict[values[1]] = values[0]
    red_button_dict.pop(values[1])

    return red_button_dict, green_button_dict

def change_on_buttons_off(window, point, red_button_dict, green_vals, green_button_dict, button_dict):
    '''
    Parameters:
    window (GraphWin): The variable name of the window
    point: the x and y values of the last place the user clicked on the screen
    red_button_dict: the dictionary that holds all the names and values for the red circles
    green_vals: the circle value of all the green circles
    green_button_dict: the dictionary that holds all the names and values for the green circles
    button_dict: the dictionary that holds the names and values of all the buttons
    
    Returns:
    dictionary: Dictionary of the red circles
    dictionary: Dictionary of the green circles
    '''
    values = change_green_to_red(window, point, green_vals, green_button_dict, button_dict)
    red_button_dict[values[1]] = values[0]
    green_button_dict.pop(values[1])
            
    return red_button_dict, green_button_dict
            
def main():
    # create the window
    window = GraphWin("Py808 Drum Sequencer", 1000, 350)
    color = color_rgb(100, 100, 255)
    window.setBackground(color)
    
    # create a Player() and SoundFile() objects
    player = Player()
    snare_sound = SoundFile('snare.wav')
    kick_sound = SoundFile('kick.wav')
    hihat_open_sound = SoundFile('hihat_open.wav')
    hihat_closed_sound = SoundFile('hihat_closed.wav')
    
    # defining color
    light_green = color_rgb(125, 255, 0)
    
    # create labels for rows 
    create_labels(window)
    
    # create start and stop buttons
    play_button, stop_button = create_start_stop_button(window)
    
    # draw the tempo entry and label
    tempo_entry = create_tempo_box_label(window)

    # draw rows of black circles to outline colored cricles
    black_button_dict = create_black_circles(window)
    
    # draw rows of step buttons
    button_dict = create_colored_buttons(window, TRACKLENGTH, BUTTONSIZE)
    
    # creating dictionaries for the green and red buttons to be stored in
    green_button_dict = {}
    red_button_dict = button_dict.copy()
    
    # A continuous loop that allows for user input 
    while True:
        # making sure the click is in a valid position
        point = window.checkMouse()
        if point != None:
            x = point.getX()
            y = point.getY()
            break_val = 1
            
            # pulling the values from the key-value pairs for teh red and green buttons
            red_vals = list(red_button_dict.values())
            green_vals = list(green_button_dict.values())
            
            # the loop will check to see if any of the red buttons were clicked on and change it to green if it was
            for red in red_vals:
                if isPointOnButton(point, red) == True:
                    red_button_dict, green_button_dict = change_off_buttons_on(window, point, red_vals, red_button_dict, green_button_dict, button_dict, light_green)
                    
            # the loop will check to see if any of the green buttons were clicked on and change it to red if it was
            for green in green_vals:    
                if isPointOnButton(point, green) == True:
                    red_button_dict, green_button_dict = change_on_buttons_off(window, point, red_button_dict, green_vals, green_button_dict, button_dict)
            
            # if the play button is pressed while the program is not playing through the track,
            # then it will start playing through the track and make appropriate sounds according to the green buttons
            if isPointOnButton(point, play_button):
                # retrive the user-decided tempo entered in the tempo box
                tempo = int(tempo_entry.getText())
                # the track will continue to loop until the stop button is pressed
                while True:
                    count = 0
                    names = []
                    green_name_list = []
                    black_vals = list(black_button_dict.values())
                    
                    # breaking out of the while loop since the stop button was pressed
                    if break_val == 0:
                        break
                        break_val = 1
                    
                    # looping through the black circles on each column at a time and changing them to yellow 
                    for black in black_vals:
                        point = window.checkMouse()
                        
                        # if the play button is pressed while the track is playing, then the tempo will be set to the tempo entered in the tempo box
                        if point != None and isPointOnButton(point, play_button) == True:
                            tempo = int(tempo_entry.getText())

                        # if the stop button was pressed than this breaks out from the process of looping through the track and sets a variable to break the enter loop.
                        if point != None and isPointOnButton(point, stop_button) == True:
                            break_val = 0
                            break
                        
                        if point != None:
                            # pulling the values from the key-value pairs for teh red and green buttons
                            red_vals = list(red_button_dict.values())
                            green_vals = list(green_button_dict.values())
                            
                            # the loop will check to see if any of the red buttons were clicked on and change it to green if it was
                            for red in red_vals:
                                if isPointOnButton(point, red) == True:
                                    red_button_dict, green_button_dict = change_off_buttons_on(window, point, red_vals, red_button_dict, green_button_dict, button_dict, light_green)
                                    
                            # the loop will check to see if any of the green buttons were clicked on and change it to green if it was         
                            for green in green_vals:    
                                if isPointOnButton(point, green) == True:
                                    red_button_dict, green_button_dict = change_on_buttons_off(window, point, red_button_dict, green_vals, green_button_dict, button_dict)
                                
                        # creating a list of the buttons that are being highlighted yellow
                        name = list(black_button_dict.keys())[black_vals.index(black)]
                        black_button_dict[name].setFill("Yellow")
                        count += 1
                        names.append(name)
                            
                        # once 4 circles have been highlighted, the appropriate sounds will be played, the code will wait some time to play the nest sound,
                        # and the highlighted yellow buttons will be changed back to black
                        if count == 4:
                            # getting the values of the green circles
                            red_vals = list(red_button_dict.values())
                            green_vals = list(green_button_dict.values())
                        
                            for green in green_vals:
                                green_name = list(green_button_dict.keys())[green_vals.index(green)]
                                green_name_list.append(green_name)
                                    
                            red_vals = list(red_button_dict.values())
                            green_vals = list(green_button_dict.values())
                            # Plays the appropriate sound for the green buttons
                            for circle_name in green_name_list:
                                if names[0] == circle_name:
                                    kick_sound.play(player)
                                if names[1] == circle_name:
                                    snare_sound.play(player)
                                if names[2] == circle_name:
                                    hihat_closed_sound.play(player)
                                if names[3] == circle_name:
                                    hihat_open_sound.play(player)                            
                            # the program will wait a certain amount of time respective of the inputed tempo
                            tempo_secs = 60/tempo/4
                            time.sleep(tempo_secs)
                            # changes the yellow circles back to black
                            for circle_name in names:
                                black_button_dict[circle_name].setFill("Black")
                                count = 0
                            # resetting the name lists
                            names = []
                            green_name_list = []
        
main()
