# Python-Beat-Sequencer
Augustana College 
CSC 201: Introduction to Computer Science 
Project
Primo Moreno

This project was assigned by my professor Dr. Peterson.
He came up with the idea of a beat sequencer, provided the WAV files and the sounds file, the doc string at the beginning, and gave us the code for isPointOnButton().
Everything else was written by me.

IMPORTANT: The Drum Sequencer Final Code Copy requires the Python packages numpy and PyAudio to run without error.

Program's Function:
The program creates a window with sixteen buttons that all initially start as off or red.
There are 4 rows of buttons and each row is linked to a different sound. 
Row 1 is a kick sound, row 2 is a snare sound, row 3 is a closed HiHat sound, and row 4 is an open HiHat sound.
At any time, the user can click on one of the red buttons to change its color to green or vice versa.

There are also two buttons above the others. 
The button on the left is the play button that starts the beat sequencer and progressively iterates through the 16 columns of buttons from left to right.
The outlines of the buttons will turn yellow when the program is looking at that column.
If a button has been clicked and turned green, then the program will notice this and play the respective sound the button should make based on the row its in.

The rate which the program iterates through the columns depends on the number inputted in the tempo box, it starts at 60 beats per minute.
If the user wishes to change the tempo, then they just need to input the desired number and click the play button. This works even if the program is already iterating through the buttons.
If the user wishes to stop the beat sequencer then all they have to do it press the stop button.

Code Aspects:
I used dictionaries to store the references to the respective buttons.
I used a dictionary for the black circles behind the red/green ones, the red circles, and the green circles. The dictionaries store the column and row of the circle in the key and the circle object in the value. Most of the code is shifting circles from one dictionary to another so that it can be read correctly by the beat sequencer.

Most of the code has comments or doc strings to describe their function.
