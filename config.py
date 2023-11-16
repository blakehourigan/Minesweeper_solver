# config.py

import platform

from pathlib import Path

# Construct an absolute path to the image
script_location = Path(__file__).resolve().parent

mine_image = str(script_location / 'assets' / 'bomb.png')
flag_image = str(script_location / 'assets' / 'flag.png')

task_tray_image = str(script_location / 'assets' / 'task_tray.png')
task_tray_image_ico = str(script_location / 'assets' / 'task_tray_ico.ico')

game_over_png = str(script_location / 'assets' / 'game_over.png')
winner_png = str(script_location / 'assets' / 'winner.png')

DIFFICULTIES = {
    "Beginner": {"size": 9, "mines": 10},
    "Intermediate": {"size": 16, "mines": 40},
    "Expert": {"size": 24, "mines": 99}
}

MINE_COLORMAP = {
    '1' : 'blue',
    '2' : 'green', 
    '3' : 'red',
    '4' : 'navy',
    '5' : 'orange red',
    'empty' : 'white',
    'mine' : 'grey',
    'flag' : 'white'
}

# GA Parameters 

POPULATION_SIZE = 250
GENERATIONS = 250
TOURNAMENT_SIZE = 75
MUTATION_RATE = 0.3
CROSSOVER_RATE = 0.7
ELITISM_COUNT = 10
ITERATIONS = 3

# gui related configuration

# main gui play buttons
button_width = 30
button_height = 30

# welcome window size

welc_width = 400
welc_height = 120

def get_task_tray_icon():
    if platform.system() == "Windows":
        return task_tray_image_ico
    else:
        return task_tray_image