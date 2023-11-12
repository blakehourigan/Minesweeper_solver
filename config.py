# config.py

from pathlib import Path

# Construct an absolute path to the image
script_location = Path(__file__).resolve().parent
mine_image = str(script_location / 'assets' / 'bomb.png')

DIFFICULTIES = {
    "Beginner": {"size": 9, "mines": 10},
    "Intermediate": {"size": 16, "mines": 40},
    "Expert": {"size": 24, "mines": 99}
}

# gui related configuration

button_width = 50
button_height = 50
