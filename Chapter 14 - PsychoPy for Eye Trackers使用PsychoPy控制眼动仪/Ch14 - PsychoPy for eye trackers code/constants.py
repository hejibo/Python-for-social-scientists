# The DISPTYPE can be either 'pygame' or 'psychopy'
DISPTYPE = 'pygame'
# The DISPSIZE should match your monitor's resolution!
DISPSIZE = (1024, 768)

# Foreground colour set to white
FGC = (255, 255, 255)
# Background colour set to black
BGC = (0, 0, 0)

# Fixation mark time (milliseconds)
FIXTIME = 2000
# Image time (milliseconds)
IMGTIME = 10000


import os
# Get the path to the current folder
DIR = os.path.dirname(os.path.abspath(__file__))
# Get the path to the image folder
IMGDIR = os.path.join(DIR, 'images')

# Get a list of all image names
IMGNAMES = os.listdir(IMGDIR)
# Sort IMGNAMES in alphabetical order
IMGNAMES.sort()